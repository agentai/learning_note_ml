#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import re
import json

from zhishikoo.items import BookListItem, BookInfoItem


class BookListSpider(scrapy.Spider):
    name = 'zhishikoo'
    allowed_domains = ['book.zhishikoo.com']
    start_urls = ['https://book.zhishikoo.com/books/category/news']

    def parse(self, response):
        books = {}
        book_paths = response.xpath("//div[@class='post grid']//a")
        for book_path in book_paths:
            book_url_info = {
                "title": book_path.xpath(".//@title").get().strip().replace(",", "，"),
                "book_url": book_path.xpath(".//@href").get().strip(),
            }
            if book_url_info["title"] in books or "https://book.zhishikoo.com/books/" not in book_url_info["book_url"]:
                continue
            book_info_item = BookListItem(
                title=book_url_info["title"], book_url=book_url_info["book_url"],
            )
            yield book_info_item
            books[book_url_info["title"]] = book_url_info
            yield scrapy.Request(url=book_url_info["book_url"], callback=self.parse_book, meta=book_url_info)

        next_page = response.xpath("//li[@class='next-page']//a//@href").get().strip()
        print("next_page", next_page)
        print("book_size", len(books))
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def get_or_default(self, src_path, xpath_str, default=""):
        tmp = src_path.xpath(xpath_str).extract()
        if not tmp:
            return default
        else:
            return " ".join([x.strip() for x in tmp])

    def parse_book(self, response):
        book_url_info = response.meta
        book_info = {
            "title": book_url_info["title"],
            "book_url": book_url_info["book_url"]
        }
        print("start", book_info["title"], response.url)
        content_path = response.xpath("//article[@class='single-content']")
        book_info["category_list"] = "->".join(response.xpath(".//div[@class='breadcrumbs']//a//text()").extract())

        for tmp_path in content_path.xpath(".//div[@class='article-meta']//span"):
            key = tmp_path.xpath(".//i//@class").get()
            value = self.get_or_default(tmp_path, ".//text()")
            if not key:
                continue
            if "dripicons-clock" in key:
                book_info["update_time"] = value
            if "dripicons-folder" in key:
                value = self.get_or_default(tmp_path, ".//a//text()")
                book_info["category"] = value
            if "dripicons-preview" in key:
                book_info["show_count"] = value
        book_info["cover_url"] = self.get_or_default(content_path, ".//img[@class='alignleft']//@src")
        tmp_paths = content_path.xpath(".//figure")
        if tmp_paths and len(tmp_paths[-1].xpath(".//strong")):
            book_info["book_property"] = " ".join(tmp_paths[-1].xpath('.//text()').extract()).strip()

        tmp_paths = content_path.xpath(".//div[@class='article-tags']//a")
        if tmp_paths:
            book_tags = {}
            for tmp_path in tmp_paths:
                book_tags[self.get_or_default(tmp_path, ".//text()")] = self.get_or_default(tmp_path, ".//@href")
            book_info["book_tags"] = json.dumps(book_tags, ensure_ascii=False)

        tmp_path = content_path.xpath(".//div[@style='float: left; margin-top: -20px;']")
        if tmp_path:
            book_describe = " ".join(
                tmp_path.xpath(".//text()").extract()
            ).strip().replace(":", "：").replace("： ", "：")\
                .replace("https：", "https:").replace("http：", "https:").replace("http:", "https:")
            book_info["book_describe"] = book_describe
            if "链接：" in book_describe:
                tmp_str = book_describe[book_describe.index("链接："):]
                book_info["pan_url"] = " ".join(re.findall(r'(https:[\S]+)', tmp_str, re.M | re.I)).strip()
                book_info["pan_extraction_code"] = " ".join(re.findall(r'提取码：([\S]+)', tmp_str, re.M | re.I)).strip()
                book_info["extracting_password"] = " ".join(re.findall(r'解压密码：([\S]+)', tmp_str, re.M | re.I)).strip()
        book_info_item = BookInfoItem(
            **book_info
        )
        yield book_info_item

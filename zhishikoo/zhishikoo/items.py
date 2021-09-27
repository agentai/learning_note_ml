# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookListItem(scrapy.Item):
    # 书名
    title = scrapy.Field()
    # 网址
    book_url = scrapy.Field()


class BookInfoItem(scrapy.Item):
    # 书名
    title = scrapy.Field()
    # 网址
    book_url = scrapy.Field()
    # 类别，例如：世界史
    category = scrapy.Field()
    # 类别路由，例如：人文社科->历史考古->世界史
    category_list = scrapy.Field()
    # 更新日期
    update_time = scrapy.Field()
    # 曝光数
    show_count = scrapy.Field()
    # 封面url
    cover_url = scrapy.Field()
    # 书基础属性
    book_property = scrapy.Field()
    # 书简介
    book_describe = scrapy.Field()
    # 网盘地址
    pan_url = scrapy.Field()
    # 提取码
    pan_extraction_code = scrapy.Field()
    # 解压秘密
    extracting_password = scrapy.Field()
    # 书标签
    book_tags = scrapy.Field()

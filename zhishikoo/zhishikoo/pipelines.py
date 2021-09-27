# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from zhishikoo.items import BookListItem, BookInfoItem
from scrapy.exporters import JsonLinesItemExporter as ItemExporter
import time


class ZhishikooPipeline:

    def open_spider(self, spider):
        self.file_book_list = open("book_list.json_{}".format(int(time.time())), "wb")
        self.exporter_book_list = ItemExporter(self.file_book_list, encoding="utf8")
        self.exporter_book_list.start_exporting()

        self.file_book_info = open("book_info.json_{}".format(int(time.time())), "wb")
        self.exporter_book_info = ItemExporter(self.file_book_info, encoding="utf8")
        self.exporter_book_info.start_exporting()

    def process_item(self, item, spider):
        if type(item) == BookListItem:
            self.exporter_book_list.export_item(item)
        if type(item) == BookInfoItem:
            self.exporter_book_info.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter_book_list.finish_exporting()
        self.exporter_book_info.finish_exporting()
        self.file_book_list.close()
        self.file_book_info.close()


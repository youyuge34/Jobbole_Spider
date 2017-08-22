# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

import MySQLdb


class JobspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """
    自定义json文件的导出
    """

    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        print 'closed'
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        # database的连接
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'article', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
              insert into jobbole_article(title, url, create_date, fav_nums)
              VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()

class JsonExporterPipeline(object):
    """
    调用scrapy提供的JsonItemExporter导出json文件
    """

    def __init__(self):
        self.file = open('articleExporter.json', 'wb')
        self.expoter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.expoter.start_exporting()

    def close_spider(self, spider):
        self.expoter.finish_exporting()
        print 'finished export'
        self.file.close()

    def process_item(self, item, spider):
        self.expoter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        item['front_image_path'] = image_paths
        return item  # 传递给下一个pipeline

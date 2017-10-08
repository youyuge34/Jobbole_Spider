# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from JobSpider.spiders.amazon import AmazonSpider

import MySQLdb
import MySQLdb.cursors


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


class MysqlTwistedPipeline(object):
    """
    利用twist的异步容器，异步写入MySQL，因为scrapy解析速度》MySQL写入速度
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        被scrapy调用，回调传入我们的settings.py
        """
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)  # 异步加载
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入， 插入逻辑封装在item中，利用多态特性降低耦合
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

class JsonExporterPipeline(object):
    """
    调用scrapy提供的JsonItemExporter导出json文件
    """

    def __init__(self):
        self.file = open(AmazonSpider.FILE_NAME, 'wb')
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
        image_paths = ''
        if "front_image_url" in item:
            image_paths = [x['path'] for ok, x in results if ok]
        item['front_image_path'] = image_paths
        return item  # 传递给下一个pipeline

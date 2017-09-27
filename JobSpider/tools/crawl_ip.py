#!/usr/bin/env python
# encoding: utf-8
"""
@author: yousheng
@contact: 1197993367@qq.com
@site: http://youyuge.cn

@version: 1.0
@license: Apache Licence
@file: crawl_ip.py
@time: 17/9/27 下午3:06

"""
import requests
import MySQLdb
from scrapy.selector import Selector
from JobSpider.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME

conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                       db=MYSQL_DBNAME, charset='utf8')
cursor = conn.cursor()


def crawl_xici_ip(pages):
    '''
    爬取一定页数上的所有代理ip,每爬完一页，就存入数据库
    :return:
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(1, pages):
        response = requests.get(url='http://www.xicidaili.com/nn/{0}'.format(i), headers=headers)

        all_trs = Selector(text=response.text).css('#ip_list tr')

        ip_list = []
        for tr in all_trs[1:]:
            ip = tr.xpath('td[2]/text()').extract_first().encode('utf8')
            port = tr.xpath('td[3]/text()').extract_first().encode('utf8')
            ip_type = tr.xpath('td[6]/text()').extract_first().encode('utf8')
            ip_speed = tr.xpath('td[7]/div/@title').extract_first()
            if ip_speed:
                ip_speed = float(ip_speed.split(u'秒')[0])
            ip_alive = tr.xpath('td[9]/text()').extract_first().encode('utf8')

            ip_list.append((ip, port, ip_type, ip_speed, ip_alive))

        # 每页提取完后就存入数据库
        for ip_info in ip_list:
            cursor.execute(
                "insert proxy_ip(ip, port, type, speed, alive) VALUES('{0}', '{1}', '{2}', {3}, '{4}')".format(
                    ip_info[0], ip_info[1], ip_info[2], ip_info[3], ip_info[4]
                )
            )

            conn.commit()


if __name__ == '__main__':
    crawl_xici_ip(pages=10)

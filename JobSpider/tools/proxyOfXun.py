#!/usr/bin/env python
# encoding: utf-8
"""
@author: yousheng
@contact: 1197993367@qq.com
@site: http://youyuge.cn

@version: 1.0
@license: Apache Licence
@file: proxyOfXun.py
@time: 17/10/10 下午8:12

"""
import sys
import time
import hashlib
import requests
from JobSpider.settings import MY_USER_AGENT
import random
from scrapy.selector import Selector
import codecs


class proxySpider():
    orderno = "ZF201710108032AMX47f"
    secret = "df6317ed89f2473d93d72c4a9ef6bb78"

    ip_port = 'forward.xdaili.cn:80'

    def __init__(self):
        self.session = requests.session()
        self.user_agent = MY_USER_AGENT
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def start_crawl(self, url):
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        sign = hashlib.md5(string).hexdigest().upper()  # 计算sign
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        agent = random.choice(self.user_agent)

        proxy = {"http": "http://" + self.ip_port, "https": "https://" + self.ip_port}
        headers = {"Proxy-Authorization": auth,
                   "User-Agent": agent, }
        r = self.session.get(url=url, headers=headers, proxies=proxy, verify=False,
                             allow_redirects=False)
        return r.text

    def saveToJson(self, dic):
        pass


if __name__ == '__main__':
    spider = proxySpider()
    response = spider.start_crawl(
        'https://www.amazon.com/PDF-Max-Annotate-documents-Forms/product-reviews/B00RDSHI66/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2')
    comments = Selector(text=response).css('#cm_cr-review_list .review')
    for selector in comments:
        dic = dict()
        author = selector.css('.author::text').extract_first('')
        title = selector.css('.review-title::text').extract_first('')
        dic['author'] = author
        dic['title'] = title

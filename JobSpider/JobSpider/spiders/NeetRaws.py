# -*- coding: utf-8 -*-
import scrapy
from urlparse import urljoin
from scrapy.http import Request


class NeetrawsSpider(scrapy.Spider):
    name = 'NeetRaws'
    allowed_domains = ['www.btbaocai.net']
    start_urls = ['http://www.btbaocai.net/search/neet-raws/?c=&s=create_time&p=1']
    mMagnetList = []
    mNameList = []

    def parse(self, response):
        names = response.css('td.x-item div a.title::text').extract()
        magnets = response.css('td.x-item div a.title::attr(href)').extract()
        size = len(names)
        for i in range(size):
            if names[i] not in self.mNameList and names[i][0] == '[':
                self.mNameList.append(names[i])
                self.mMagnetList.append('magnet:?xt=urn:btih:' + magnets[i][6:])
        next_url = response.css('ul.pagination li a::attr(href)').extract()[-1]
        if (next_url == '#'):
            self.saveToFile()
        next_url = urljoin(response.url, next_url)
        yield Request(url=next_url, callback=self.parse)

    def saveToFile(self):
        with open('NeetMagnet', 'w') as f:
            for magnet in self.mMagnetList:
                f.write(magnet)
                f.write('\n')
            for name in self.mNameList:
                f.write(name.encode('utf8'))
                f.write('\n')

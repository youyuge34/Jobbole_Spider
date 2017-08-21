# -*- coding: utf-8 -*-
import scrapy


class NeetrawsSpider(scrapy.Spider):
    name = 'NeetRaws'
    allowed_domains = ['https://btso.pw/search/Neet-raws']
    start_urls = ['http://https://btso.pw/search/Neet-raws/']

    def parse(self, response):
        pass

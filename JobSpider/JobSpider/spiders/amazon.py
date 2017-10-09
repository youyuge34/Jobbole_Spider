# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy.http import Request
import urlparse
from JobSpider.items import AmazonRevItem, ReviewItemLoader
import logging
from JobSpider.utils.common import get_md5
from JobSpider.settings import SQL_DATETIME_FORMAT,project_dir
import os

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    FILE_NAME = 'Downloader.json'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/AFTVnews-com-Downloader/dp/B01N0BP507/ref=zg_bs_mobile-apps_f_1?_encoding=UTF8&psc=1&refRID=3NV5QGMA8TBWG65KNRMD']
    logger = logging.getLogger('amazon_spider')

    def __init__(self):
        from selenium import webdriver

        self.browser = webdriver.Edge(
            executable_path='F:/PythonProjects/Scrapy_Job/JobSpider/tools/MicrosoftWebDriver.exe')

        # 设置chromedriver不加载图片
        # chrome_opt = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images":2}
        # chrome_opt.add_experimental_option("prefs", prefs)
        #
        # self.browser = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(project_dir),'tools\chromedriver.exe'),chrome_options=chrome_opt)
        super(AmazonSpider, self).__init__()

        from scrapy.xlib.pydispatch import dispatcher
        from scrapy import signals

        # 绑定信号量，当spider关闭时调用我们的函数
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print 'spider closed'
        self.browser.quit()

    def parse(self, response):
        '''
        第一个回调函数
        :param response:
        :return:
        '''
        if u'product-reviews' in response.url:
            # print 'into parse_detail'
            # asinTitle = response.css('.product-title a::text').extract_first('').encode('utf8')
            yield Request(url=response.url,callback=self.parse_detail)
        else:
            # asinTitle = response.css('#btAsinTitle::text').extract_first('').encode('utf8')
            commentUrl = response.css('#reviews-medley-footer .a-link-emphasis::attr(href)').extract_first('').encode('utf8')
            if commentUrl is not None:
                yield Request(url=urlparse.urljoin(response.url, commentUrl),callback=self.parse_detail)
            else:
                self.logger.warn('cannot find all comments page')

        #在配置文件中配置输出json文件名
        # if asinTitle:
        #     self.FILE_NAME = asinTitle.strip()+'.json'
        # else:
        #     self.FILE_NAME = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)+'.json'
        # print self.FILE_NAME


    def parse_detail(self, response):
        '''
        如果是评论页
        :param response:
        :return:
        '''
        comments = response.css('#cm_cr-review_list .review')
        for comment in comments:
            itemLoader = ReviewItemLoader(item=AmazonRevItem(), response=response, selector=comment)
            itemLoader.add_css('rating', '.a-icon-alt::text')
            itemLoader.add_css('title', '.review-title::text')
            rev_url = urlparse.urljoin(response.url,comment.css('.review-title::attr(href)').extract_first(''))
            itemLoader.add_value('url', rev_url)
            itemLoader.add_value('url_object_id', get_md5(rev_url))
            itemLoader.add_css('author', '.author::text')
            itemLoader.add_css('date', '.review-date::text')
            itemLoader.add_css('content', '.review-text::text')
            itemLoader.add_css('votes','.review-votes::text')
            itemLoader.add_value('crawl_time',datetime.datetime.now())

            answer_item = itemLoader.load_item()
            yield answer_item


        next_urls = response.css('#cm_cr-pagination_bar .a-last a::attr(href)').extract_first('').encode('utf8')
        if next_urls:
            yield Request(url=urlparse.urljoin(response.url, next_urls), callback=self.parse_detail)
        else:
            self.logger.info('no more page!!!')
            # print response.text
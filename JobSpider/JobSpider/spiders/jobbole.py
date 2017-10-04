# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import urlparse
from JobSpider.items import JobBoleArticleItem, ArticleItemLoader
from JobSpider.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/page/1']

    # def __init__(self):
    #     from selenium import webdriver
    #
    #     self.browser = webdriver.Edge(
    #         executable_path='F:/PythonProjects/Scrapy_Job/JobSpider/tools/MicrosoftWebDriver.exe')
    #     super(JobboleSpider, self).__init__()
    #
    #     from scrapy.xlib.pydispatch import dispatcher
    #     from scrapy import signals
    #
    #     # 绑定信号量，当spider关闭时调用我们的函数
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     print 'spider closed'
    #     self.browser.quit()

    # 收集伯乐在线所有404的url以及404页面数
    handle_httpstatus_list = [404]

    def __init__(self, **kwargs):
        from scrapy.xlib.pydispatch import dispatcher
        from scrapy import signals
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        super(JobboleSpider, self).__init__()

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))
        print 'failed urls:' + self.crawler.stats.get_value('failed_urls')

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        """
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            # yield 直接交给scrapy进行下载
            yield Request(url=urlparse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
            # print post_url

        # 提取下一页面交给scrapy
        next_urls = response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_urls:
            yield Request(url=urlparse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_detail(self, response):
        """
        解析文章详情页面的信息,是下载后的回调函数
        :param response:
        :return:
        """
        article_item = JobBoleArticleItem()  # 实例化
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·",
        #                                                                                                             "").strip()
        # praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        #
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # # 过滤掉收藏数里的中文字
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # # 评论数
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # # 正文
        # content = response.xpath("//div[@class='entry']").extract()[0]
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith(u"评论")]
        # tags = ",".join(tag_list)
        #
        # article_item["title"] = title
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(url=response.url)
        # try:
        #     create_date = datetime.datetime.strptime(create_date.encode('utf-8'), '%Y/%m/%d ·').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]  # 必须要是list形式才能用内置的images pipeline
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

        # 通过自定义的Itemloader加载item

        front_image_url = response.meta.get('front_image_url', '')  # 文章封面图
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        # yield继续会传递到pipelines中
        yield article_item

        # 通过css选择器提取字段
        # front_image_url = response.meta.get("front_image_url", "")  #文章封面图
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
        # praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css(".bookmark-btn::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.css("div.entry").extract()[0]
        #
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith(u"评论")]
        # tags = ",".join(tag_list)
        # print title
        # print create_date
        # print praise_nums
        # print fav_nums
        # print comment_nums
        # print tags

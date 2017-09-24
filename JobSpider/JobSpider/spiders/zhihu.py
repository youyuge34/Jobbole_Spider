# -*- coding: utf-8 -*-
import json

import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    header = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        pass

    def start_requests(self):
        # spider启动时的调用函数,先去登陆页面获取xsrf
        return [scrapy.Request("https://www.zhihu.com", headers=self.header, callback=self.login)]

    def login(self, response):
        '''
        获取验证码，传递给下一个函数
        :return:
        '''
        xsrf = response.xpath("//input[@name='_xsrf']/@value").extract_first()
        print 'xsrf----> ', xsrf

        if xsrf:
            post_url = 'https://www.zhihu.com/login/phone_num'
            post_data = {
                "_xsrf": xsrf,
                "phone_num": '18362933375',
                "password": 'qwert12345',
                "captcha": ''
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.header, meta={"post_data": post_data},
                                 callback=self.login_after_captcha)  # meta数据可传递给下一个callback函数

        else:
            raise Exception('xsrf is none')

    def login_after_captcha(self, response):
        '''
        实际的登陆函数，手动输入验证码
        :param response:
        :return:
        '''
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = raw_input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})  # 从上一个函数传递过来的meta
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]

    def check_login(self, response):
        '''
        验证服务器返回的数据，判断登录是否成功
        :return:
        '''
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"].encode('utf-8') == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)

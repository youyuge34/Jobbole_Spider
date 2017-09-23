# encoding: utf-8
"""
@author: yousheng
@contact: 1197993367@qq.com
@site: http://youyuge.cn

@version: 1.0
@license: Apache Licence
@file: zhihu_login_request.py
@time: 17/9/23 上午10:09

"""
import requests
import re
from scrapy.selector import Selector

try:
    import cookielib
except:
    import http.cookiejar as cookielib

# 代表一次长连接请求，下面都用session代替requests发起请求
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print 'cookie is not loaded'

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent
}


def is_login():
    # 通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/question/56250357/answer/148534773"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_xsrf():
    '''
    从登陆的网页源代码中获取xsrf code
    '''
    response = session.get("https://www.zhihu.com", headers=header)
    value = Selector(text=response.text).xpath("//input[@name='_xsrf']/@value").extract_first()
    # match_obj = re.match(r'.*name="_xsrf" value="(.*?)"', response.text)
    print value
    if value:
        return value
    else:
        return ''


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print ("ok")


def get_captcha():
    '''
    获取验证码
    :return: 手动输入验证码的值
    '''
    import time
    t = str(int(time.time() * 1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = raw_input("输入验证码\n>")
    return captcha


def login_in(account, password):
    '''
    模拟知乎登陆
    :param account: 账号
    :param password: 密码
    :return:
    '''
    if re.match('^1\d{10}', account):
        print '手机号登陆------->'
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha()
        }
    else:
        # 判断用户名是否为邮箱
        if "@" in account:
            print("邮箱方式登录")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                "captcha": get_captcha()
            }

    response_text = session.post(url=post_url, data=post_data, headers=header)
    session.cookies.save()


# get_xsrf()
login_in('18362933375', 'qwert12345')
# get_index()

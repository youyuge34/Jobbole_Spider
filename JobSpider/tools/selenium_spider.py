#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-09-30 12:48
# @Author  : YouSheng

from selenium import webdriver
from scrapy.selector import Selector
import time

browser = webdriver.Edge(executable_path='F:/PythonProjects/Scrapy_Job/JobSpider/tools/MicrosoftWebDriver.exe')


def testTaobao():
    '''
    获取淘宝商品的价格信息
    :return:
    '''
    browser.get('https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-15339356944.47.54870883CGrLWt&id=554553313519')

    t_selector = Selector(text=browser.page_source)
    print t_selector.css('#J_PromoPriceNum::text').extract_first()
    # print browser.page_source

    browser.quit()


def zhihulogin():
    '''
    模拟知乎登陆
    '''
    browser.get('https://www.zhihu.com/#signin')
    browser.implicitly_wait(3)
    # browser.find_element_by_css_selector('.qrcode-signin-container .signin-switch-password').click()
    browser.find_element_by_css_selector('.view-signin input[name="account"]').send_keys('18362933375')
    browser.find_element_by_css_selector('.view-signin input[name="password"]').send_keys('')

    browser.find_element_by_css_selector('.view-signin button.sign-button').click()


def weibo_login():
    '''
    selenium完成微博模拟登陆
    :return:
    '''
    browser.implicitly_wait(5)
    browser.get('http://weibo.com/')
    # browser.implicitly_wait(5)
    time.sleep(4)
    browser.find_element_by_css_selector('#loginname').clear()
    browser.find_element_by_css_selector('.info_list.password input[name="password"]').clear()

    browser.find_element_by_css_selector('#loginname').send_keys('1197993367@qq.com')
    browser.find_element_by_css_selector('.info_list.password input[name="password"]').send_keys('')
    browser.find_element_by_css_selector('.info_list.login_btn a[node-type="submitBtn"]').click()


def oschina_auto_scroll():
    '''
    自动页面下滑到底部，直接用js代码
    :return:
    '''
    browser.get("http://www.oschina.net/blog")
    for i in range(3):
        print i
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        time.sleep(3)


def test_phantomjs():
    '''
    无界面浏览器，适合centerOS等无界面系统，多进程情况下phantomjs性能会下降很严重
    :return:
    '''
    browser = webdriver.PhantomJS(executable_path="F:/PythonProjects/Scrapy_Job/JobSpider/tools/phantomjs.exe")
    browser.get(
        "https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025")

    print (browser.page_source)
    browser.quit()

if __name__ == '__main__':
    # testTaobao()
    # zhihulogin()
    # weibo_login()
    # oschina_auto_scroll()
    test_phantomjs()

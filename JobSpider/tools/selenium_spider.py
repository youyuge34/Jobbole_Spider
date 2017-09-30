#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-09-30 12:48
# @Author  : YouSheng

from selenium import webdriver

browser = webdriver.Edge(executable_path='F:/PythonProjects/Scrapy_Job/JobSpider/tools/MicrosoftWebDriver.exe')

browser.get(
    'https://item.taobao.com/item.htm?spm=a217h.9580640.831217.1.364947ad4LKVyV&scm=1007.12144.81309.70043_0&pvid=b6e1fb88-83f4-43c8-b585-935eef034d64&id=557019864875')

print browser.page_source

browser.quit()

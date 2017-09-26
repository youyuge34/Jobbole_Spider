#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-08-19 19:16
# @Author  : YouSheng
__author__ = 'YouSheng'

#用此文件代替执行cmd命令行命令，有助于debug
from scrapy.cmdline import execute
import sys
import os

#设置cmd主目录，这样调用execute才会生效
# sys.path.append('F:\PythonProjects\Scrapy_Job\JobSpider')
sys.path.append(os.path.dirname(os.path.abspath(__file__))) #动态获取本文件的父文件夹路径

# execute(['scrapy','crawl','jobbole'])
# execute(['scrapy','crawl','zhihu'])
execute(['scrapy', 'crawl', 'lagou'])

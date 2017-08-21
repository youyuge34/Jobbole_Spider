#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-08-21 9:45
# @Author  : YouSheng
import hashlib


def get_md5(url):
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print get_md5('http://jobbole.com')

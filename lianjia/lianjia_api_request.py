#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author : Zhou Jian
@email  : summychou@163.com
'''

import time

try:
    from selenium import webdriver
except ImportError, e:
    print '>> selenium Module is not found, please install it first'

try:
    from tqdm import tqdm
except ImportError, e:
    print '>> tqdm Module is not found, please install it first'

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'gz.lianjia.com',
    'Referer': 'http://gz.lianjia.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def run():
    driver = webdriver.PhantomJS()
    driver.set_window_size(800, 600)
    driver.get('http://gz.lianjia.com/api/newhouserecommend?type=1&query=http://gz.lianjia.com/ershoufang/pg1/')
    print driver.page_source
        
if __name__ == '__main__':
    run()

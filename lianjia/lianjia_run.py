#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author : Zhou Jian
@email  : summychou@163.com
'''

import time

try:
    from tqdm import tqdm
except ImportError, e:
    print '>> tqdm Module is not found, please install it first'

from lianjia import LianJiaSpider

def run():
    citys = ['bj', 'gz', 'sz', 'hz', 'wh']
    special_city = ['sh']
    website = '.lianjia.com'

    for city in tqdm(citys):
        print u'Crawling from {}'.format(city)

        crawler = LianJiaSpider(city, website)
        crawler.run()
        crawler.anti_crawl()
        
if __name__ == '__main__':
    run()

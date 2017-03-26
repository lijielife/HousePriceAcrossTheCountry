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

from anjuke import AnJuKeSpider

def run():
    # first_stair_citys = ['BeiJing', 'ShangHai', 'GuangZhou', 'ShenZhen', 'TianJin']
    # second_stair_citys = ['HangZhou', 'NanJing', 'JiNan', 'ChongQing', 'DaLian', 'WuHan']
    # citys = first_stair_citys + second_stair_citys
    
    citys = ['BeiJing', 'ShangHai', 'GuangZhou', 'ShenZhen', 'HangZhou', 'WuHan']
    website = '.anjuke.com'

    for city in tqdm(citys):
        print u'Crawling from {}'.format(city)

        crawler = AnJuKeSpider(city, website)
        crawler.run()

        time.sleep(1)

if __name__ == '__main__':
    run()

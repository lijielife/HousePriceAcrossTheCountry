# -*- coding: utf-8 -*-

'''
@author : Zhou Jian
@email  : summychou@163.com
'''

import warnings
warnings.filterwarnings('ignore')

import time
import random
from collections import deque
from Queue import Queue

try:
    import requests
except ImportError, e:
    print '>> requests Module is not found, please install it first'
try:
    from bs4 import BeautifulSoup
except ImportError, e:
    print '>> bs4 Module is not found, please install it first'

city_reference = {'BeiJing': u'北京', 'ShangHai': u'上海', 'GuangZhou': u'广州', 'ShenZhen': u'深圳', 'TianJin': u'',
                  'HangZhou': u'杭州', 'NanJing': u'南京', 'JiNan': u'济南', 'ChongQing': u'重庆', 'QingDao': u'青岛',
                  'DaLian': u'大连', 'NingBo': u'宁波', 'XiaMen': u'厦门', 'WuHan': u'武汉'}

# UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36'

class AnJuKeSpider(object):

    def __init__(self, city, website):
        print u'正在初始化爬虫 ...'
        self._city = city
        self._website = website
        self._root_url = 'http://' + self._city.lower() + self._website
        self._status_code = requests.get(self._root_url, headers={'User-Agent': UserAgent}).status_code
        self._spider_pipeline = Queue()
        self._put_to_pipeline(self._root_url)
    
    def __new__(cls, *args, **kwargs):
        print u'正在创建新的爬虫 ...'
        return object.__new__(cls, *args, **kwargs)

    def __del__(self):
        print u'{0}的房价抓取完毕!'.format(city_reference[self._city])

    def _put_to_pipeline(self, link):
        self._spider_pipeline.put(link)

    def _get_from_pipeline(self):
        return self._spider_pipeline.get()

    def _pipeline_length(self):
        return self._spider_pipeline.qsize()

    def _pipeline_is_empty(self):
        return self._spider_pipeline.empty()

    def _worker(self): 
        print u'正在抓取{0}的房价...'.format(city_reference[self._city])
        current_link = self._get_from_pipeline()
        headers = {
            'Host': self._city.lower() + self._website,
            'Referer': self._root_url,
            'User-Agent': UserAgent,
        }
        response = requests.get(current_link, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf8')
        navigation_bar = soup.find(name='div', attrs={'id': 'glbNavigation'})
        for a in navigation_bar.find_all(name='a', attrs={'class': 'a_navnew'})[1:4]:
            self._put_to_pipeline(a['href'])

        self._sub_worker()

    def _sub_worker(self):
        self._crawl_from_new_house_page()
        self._crawl_from_second_house_page()
        self._crawl_from_renting_house_page()

    def _crawl_from_new_house_page(self):
        current_sub_link = self._get_from_pipeline()
        crawl_link = current_sub_link + '?from=navigation'

        headers = {
            'Host': self._city.lower() + self._website,
            'Referer': crawl_link,
            'User-Agent': UserAgent,
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf8')
        link = current_sub_link
        next_link = soup.find(name='a', attrs={'class': 'next-page next-link'})['href']
        counter = 1

        with open('anjuke_new_house/{0}{1}.txt'.format(self._city, counter), 'w+') as fp:
            fp.write(response.text.encode('utf-8'))
        
        self.recursive_crawl_from_new_house_page(current_sub_link, link, next_link, counter)

    def recursive_crawl_from_new_house_page(self, root_link, pre_link, link, counter):
        current_sub_link = link
        crawl_link = current_sub_link

        headers = {
            'Host': self._city.lower() + self._website,
            'Referer': pre_link,
            'User-Agent': UserAgent,
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf8')
        link = current_sub_link

        try:
            next_link = soup.find(name='a', attrs={'class': 'next-page next-link'})['href']
            counter += 1

            with open('anjuke_new_house/{0}{1}.txt'.format(self._city, counter), 'w+') as fp:
                fp.write(response.text.encode('utf-8'))

                self.recursive_crawl_from_new_house_page(root_link, link, next_link, counter)
        except TypeError:
            pass

    def _crawl_from_second_house_page(self):
        current_sub_link = self._get_from_pipeline()
        crawl_link = current_sub_link + '?from=navigation'

        headers = {
            'Host': self._city.lower() + self._website,
            'Referer': self._root_url + '/',
            'User-Agent': UserAgent,
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf8')
        link = current_sub_link
        next_link = soup.find(name='a', attrs={'class': 'aNxt'})['href']
        counter = 1

        with open('anjuke_second_house/{0}{1}.txt'.format(self._city, counter), 'w+') as fp:
            fp.write(response.text.encode('utf-8'))
        
        self.recursive_crawl_from_second_house_page(current_sub_link, link, next_link, counter)

    def recursive_crawl_from_second_house_page(self, root_link, pre_link, link, counter):
        current_sub_link = link
        crawl_link = current_sub_link

        headers = {
            'Host': self._city.lower() + self._website,
            'Referer': pre_link,
            'User-Agent': UserAgent,
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf8')
        link = current_sub_link

        try:
            next_link = soup.find(name='a', attrs={'class': 'aNxt'})['href']
            counter += 1

            with open('anjuke_second_house/{0}{1}.txt'.format(self._city, counter), 'w+') as fp:
                fp.write(response.text.encode('utf-8'))
            
            self.recursive_crawl_from_second_house_page(root_link, link, next_link, counter)
        except TypeError:
            pass

    def _crawl_from_renting_house_page(self):
        self._get_from_pipeline()
        self._get_from_pipeline()

        current_sub_link = self._get_from_pipeline()
        crawl_link = current_sub_link + '?from=navigation'

        headers = {
            'Host': self._city.lower() + self._website,
            'Referer': self._root_url + '/',
            'User-Agent': UserAgent,
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf8')
        link = current_sub_link
        next_link = soup.find(name='a', attrs={'class': 'aNxt'})['href']
        counter = 1

        with open('anjuke_renting_house/{0}{1}.txt'.format(self._city, counter), 'w+') as fp:
            fp.write(response.text.encode('utf-8'))
        
        self.recursive_crawl_from_renting_house_page(current_sub_link, link, next_link, counter)

    def recursive_crawl_from_renting_house_page(self, root_link, pre_link, link, counter):
        current_sub_link = link
        crawl_link = current_sub_link
        headers = {
            'Host': self._city.lower() + self._website,
            'Referer': pre_link,
            'User-Agent': UserAgent,
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf8')
        link = current_sub_link

        try:
            next_link = soup.find(name='a', attrs={'class': 'aNxt'})['href']
            counter += 1

            with open('anjuke_renting_house/{0}{1}.txt'.format(self._city, counter), 'w+') as fp:
                fp.write(response.text.encode('utf-8'))
            
            self.recursive_crawl_from_renting_house_page(root_link, link, next_link, counter)
        except TypeError:
            pass

    def anti_crawl(self):
        time.sleep(random.randint(1, 2))

    def run(self):
        print u'正在连接{0}子网址，响应状态码为{1}'.format(city_reference[self._city], self._status_code)
        if self._status_code == 200:
            self._worker()
        else:
            print u'{0}子网址连接错误'.format(city_reference[self._city])

    @staticmethod
    def get_current_time():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

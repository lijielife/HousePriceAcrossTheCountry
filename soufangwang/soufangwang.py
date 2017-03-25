# -*- coding: utf-8 -*-
from collections import deque
from bs4 import BeautifulSoup
import random
import requests
import time

city_reference = {'Bei Jing': u'北京', 'Shang Hai': u'上海', 'Guang Zhou': u'广州', 'Shen Zhen': u'深圳', 'Tian Jin': u'',
                  'Hang Zhou': u'杭州', 'Nan Jing': u'南京', 'Ji Nan': u'济南', 'Chong Qing': u'重庆', 'Qing Dao': u'青岛',
                  'Da Lian': u'大连', 'Ning Bo': u'宁波', 'Xia Men': u'厦门', 'Wu Han': u'武汉'}


class SouFangWang(object):
    def __init__(self, city, website, counter):
        print u'正在初始化爬虫...'
        self.city = city
        self.website = website
        self.counter = counter
        self.root_url = 'http://' + self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website
        self.status_code = requests.get(self.root_url).status_code
        self.spider_pipeline = deque()
        self.add_to_pipeline(self.root_url)

    def __new__(cls, *args, **kwargs):
        print u'正在创建新的爬虫...'
        return object.__new__(cls, *args, **kwargs)

    def __del__(self):
        print u'{0}的房价抓取完毕!'.format(city_reference[self.city])

    @property
    def get_current_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def add_to_pipeline(self, link):
        self.spider_pipeline.append(link)

    def pop_from_pipeline(self):
        return self.spider_pipeline.popleft()

    def pipeline_length(self):
        return len(self.spider_pipeline)

    def pipeline_is_empty(self):
        return len(self.spider_pipeline) is 0

    def worker(self):
        print u'正在抓取{0}的房价...'.format(city_reference[self.city])
        current_link = self.pop_from_pipeline()
        headers = {
            'Host': self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website,
            'Referer': self.root_url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/50.0.'
                          '2661.102 Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(current_link, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding=response.encoding)
        sub_navigation = soup.find(name='div', attrs={'class': 'subnav'})
        for j, dl in enumerate(sub_navigation.find_all(name='dl')[:2]):
            if j == 0:
                if self.city == 'Bei Jing' or self.city == 'Tian Jin':
                    new_house_link = dl.find(name='dd').find_all(name='p')[1].find_all(name='a')[1]
                    self.add_to_pipeline(self.root_url + new_house_link['href'])
                    second_house_link = dl.find(name='dd').find_all(name='p')[1].find_all(name='a')[0]
                    self.add_to_pipeline(self.root_url + second_house_link['href'])
                else:
                    new_house_link = dl.find(name='dd').find_all(name='p')[1].find_all(name='a')[1]
                    self.add_to_pipeline(self.root_url + new_house_link['href'])
                    second_house_link = dl.find(name='dd').find_all(name='p')[0].find_all(name='a')[0]
                    self.add_to_pipeline(self.root_url + second_house_link['href'])
            else:
                joint_rent_link = dl.find(name='dd').find_all(name='p')[1].find_all(name='a')[0]
                self.add_to_pipeline(self.root_url + joint_rent_link['href'])
                total_rent_link = dl.find(name='dd').find_all(name='p')[0].find_all(name='a')[0]
                self.add_to_pipeline(self.root_url + total_rent_link['href'])
        self.sub_worker()

    def sub_worker(self):
        self.crawl_from_new_house_page()
        self.crawl_from_second_house_page()
        self.crawl_from_renting_house_page()
        self.crawl_from_renting_house_page()

    def crawl_from_new_house_page(self):
        current_sub_link = self.pop_from_pipeline()
        crawl_link = current_sub_link

        headers = {
            'Host': self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website,
            'Referer': self.root_url + '/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                          'Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding=response.encoding)
        link = current_sub_link
        next_link = self.root_url + soup.find(name='div', attrs={'class': 'page_nav'}).find(
            name='li', attrs={'class': 'right'}).find(name='a')['href']
        counter = 1
        with open('soufangwang_new_house/{0}.txt'.format(self.city + str(counter)), 'w+') as fp:
            fp.write(response.text.encode('utf-8'))
        self.recursive_crawl_from_new_house_page(link, next_link, counter)

    def recursive_crawl_from_new_house_page(self, pre_link, link, counter):
        current_sub_link = link
        crawl_link = current_sub_link
        headers = {
            'Host': self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website,
            'Referer': pre_link,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                          'Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding=response.encoding)
        link = current_sub_link
        try:
            next_link = self.root_url + soup.find(name='div', attrs={'class': 'page_nav'}).find(
                name='li', attrs={'class': 'right'}).find(name='a')['href']
            counter += 1
            with open('soufangwang_new_house/{0}.txt'.format(self.city + str(counter)), 'w+') as fp:
                fp.write(response.text.encode('utf-8'))
            self.recursive_crawl_from_new_house_page(link, next_link, counter)
        except AttributeError:
            next_link_li = soup.find(name='div', attrs={'class': 'page_nav'}).find_all(name='li')[-2]
            try:
                counter += 1
                with open('soufangwang_new_house/{0}.txt'.format(self.city + str(counter)), 'w+') as fp:
                    fp.write(response.text.encode('utf-8'))
                next_link = self.root_url + next_link_li.find(name='a')['href']
                self.recursive_crawl_from_new_house_page(link, next_link, counter)
            except Exception:
                pass

    def crawl_from_second_house_page(self):
        current_sub_link = self.pop_from_pipeline()
        crawl_link = current_sub_link

        headers = {
            'Host': self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website,
            'Referer': self.root_url + '/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                          'Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding=response.encoding)
        link = current_sub_link
        next_link = self.root_url + soup.find(name='div', attrs={'class': 'page_nav'}).find(
            name='li', attrs={'class': 'right'}).find(name='a')['href']
        counter = 1
        with open('soufangwang_second_house/{0}.txt'.format(self.city + str(counter)), 'w+') as fp:
            fp.write(response.text.encode('utf-8'))
        self.recursive_crawl_from_second_house_page(link, next_link, counter)

    def recursive_crawl_from_second_house_page(self, pre_link, link, counter):
        current_sub_link = link
        crawl_link = current_sub_link
        headers = {
            'Host': self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website,
            'Referer': pre_link,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                          'Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding=response.encoding)
        link = current_sub_link
        try:
            next_link = self.root_url + soup.find(name='div', attrs={'class': 'page_nav'}).find(
                name='li', attrs={'class': 'right'}).find(name='a')['href']
            counter += 1
            with open('soufangwang_second_house/{0}.txt'.format(self.city + str(counter)), 'w+') as fp:
                fp.write(response.text.encode('utf-8'))
            self.recursive_crawl_from_second_house_page(link, next_link, counter)
        except AttributeError:
            next_link_li = soup.find(name='div', attrs={'class': 'page_nav'}).find_all(name='li')[-2]
            try:
                counter += 1
                with open('soufangwang_second_house/{0}.txt'.format(self.city + str(counter)), 'w+') as fp:
                    fp.write(response.text.encode('utf-8'))
                next_link = self.root_url + next_link_li.find(name='a')['href']
                self.recursive_crawl_from_second_house_page(link, next_link, counter)
            except Exception:
                pass

    def crawl_from_renting_house_page(self):
        current_sub_link = self.pop_from_pipeline()
        crawl_link = current_sub_link

        headers = {
            'Host': self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website,
            'Referer': self.root_url + '/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                          'Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding=response.encoding)
        link = current_sub_link
        try:
            next_link = self.root_url + soup.find(name='div', attrs={'class': 'page_nav'}).find(
                name='li', attrs={'class': 'right'}).find(name='a')['href']
            with open('soufangwang_renting_house/{0}.txt'.format(self.city + str(self.counter)), 'w+') as fp:
                fp.write(response.text.encode('utf-8'))
            self.recursive_crawl_from_renting_house_page(link, next_link)
        except Exception:
            try:
                next_link = self.root_url + soup.find(name='div', attrs={'class': 'page_nav'}).find_all(
                    name='li')[-2].find(name='a')['href']
                with open('soufangwang_renting_house/{0}.txt'.format(self.city + str(self.counter)), 'w+') as fp:
                    fp.write(response.text.encode('utf-8'))
                self.recursive_crawl_from_renting_house_page(link, next_link)
            except Exception:
                pass

    def recursive_crawl_from_renting_house_page(self, pre_link, link):
        current_sub_link = link
        crawl_link = current_sub_link
        headers = {
            'Host': self.city.lower().split()[0][0] + self.city.lower().split()[1][0] + self.website,
            'Referer': pre_link,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                          'Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(crawl_link, headers=headers)
        print u'当前爬取网址 {0}'.format(crawl_link)
        print u'当前爬取状态码{0}'.format(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml', from_encoding=response.encoding)
        link = current_sub_link
        try:
            next_link = self.root_url + soup.find(name='div', attrs={'class': 'page_nav'}).find(
                name='li', attrs={'class': 'right'}).find(name='a')['href']
            self.counter += 1
            with open('soufangwang_renting_house/{0}.txt'.format(self.city + str(self.counter)), 'w+') as fp:
                fp.write(response.text.encode('utf-8'))
            self.recursive_crawl_from_renting_house_page(link, next_link)
        except AttributeError:
            next_link_li = soup.find(name='div', attrs={'class': 'page_nav'}).find_all(name='li')[-2]
            try:
                self.counter += 1
                with open('soufangwang_renting_house/{0}.txt'.format(self.city + str(self.counter)), 'w+') as fp:
                    fp.write(response.text.encode('utf-8'))
                next_link = self.root_url + next_link_li.find(name='a')['href']
                self.recursive_crawl_from_renting_house_page(link, next_link)
            except Exception:
                pass

    def anti_crawl(self):
        time.sleep(random.randint(1, 2))

    def run(self):
        print self.get_current_time
        print u'正在连接{0}子网址，响应状态码为{1}'.format(city_reference[self.city], self.status_code)
        if self.status_code == 200:
            self.worker()

        else:
            print u'{0}子网址连接错误'.format(city_reference[self.city])

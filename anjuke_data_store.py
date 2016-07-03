#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from mysql import MySql
from multiprocessing.dummy import Pool as ThreadPool
import os


def read_file(filename):
    with open('anjuke_new_house/'+filename, 'r') as fp:
        html = fp.read()
    return html


def anjuke_new_house_data_extract(soup):
    for _, _, files in os.walk('anjuke_new_house/'):
        files_list = files
    pool = ThreadPool(4)
    soup_list = pool.map(read_file, files_list)
    pool.close()
    pool.join()


def main():

    pool = ThreadPool(4)
    pool.map(dom_node_extract, soup_list)
    pool.close()
    pool.join()
    with open('anjuke_new_house/Bei Jing1.txt', 'r') as fp:
        html = fp.read()
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    for item in soup.find(name='div', attrs={'class': 'key-list'}).find_all(name='div', attrs={'class': 'item-mod'}):
        information = item.find(name='div', attrs={'class': 'infos'})
        # 楼盘名称
        loupan_name = information.find(name='div', attrs={'class': 'lp-name'}).find(name='h3').get_text().strip()
        # 楼盘对应的详细网页
        loupan_name_detail = information.find(name='div', attrs={'class': 'lp-name'}).find(name='h3')\
            .find(name='a')['href']
        # 楼盘状态
        status = [x.get_text().encode('utf8').strip() for x in
                  information.find(name='div', attrs={'class': 'lp-name'}).find_all(name='i')]
        # 楼盘地址
        address = information.find_all(name='p')[0].get_text().strip().split(']')[0][1:].strip()
        try:
            tag_panel = information.find(name='div', attrs={'class': 'tag-panel'})
            # 楼盘标签
            tags = [x.get_text().encode('utf8').strip() for x in tag_panel.find_all(name='span')]
        except AttributeError:
            tags = [u'无']
        # 楼盘售价
        price = item.find(name='div', attrs={'class': 'favor-pos'}).find_all(name='p')[0].get_text().strip()


if __name__ == '__main__':
    anjuke_new_house_data_extract()

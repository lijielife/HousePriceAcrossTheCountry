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


def read_file_in_multiprocess():
    files_list = object
    for _, _, files in os.walk('anjuke_new_house/'):
        files_list = files
    pool = ThreadPool(4)
    html_list = pool.map(read_file, files_list)
    pool.close()
    pool.join()
    return html_list


def anjuke_new_house_data_extract(html):
    temp_list = []
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    for item in soup.find(name='div', attrs={'class': 'key-list'}).find_all(name='div', attrs={'class': 'item-mod'}):
        information = item.find(name='div', attrs={'class': 'infos'})
        # 楼盘名称
        loupan_name = information.find(name='div', attrs={'class': 'lp-name'}).find(name='h3').get_text().strip()
        # 楼盘对应的详细网页
        loupan_name_detail = information.find(name='div', attrs={'class': 'lp-name'}).find(name='h3') \
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
        temp_list.append((loupan_name, loupan_name_detail, address, price))
    return temp_list


def anjuke_new_house_data_extract_in_multiprocess():
    html_list = read_file_in_multiprocess()
    pool = ThreadPool(4)
    data_list = pool.map(anjuke_new_house_data_extract, html_list)
    pool.close()
    pool.join()
    data_warehosue = []
    for data_seg_list in data_list:
        data_warehosue.extend(data_seg_list)
    return data_warehosue


def main():
    data_warehosue = anjuke_new_house_data_extract_in_multiprocess()
    d = MySql(host='121.42.188.55', port=3306,
              username='root', password='tianchi',
              charset="utf8")
    d.connect_to_database_server()
    d.change_database('AnJuKe')
    sql = "INSERT INTO AnJuKe_New_House(loupan_name, loupan_name_detail, address, price) VALUES(%s, %s, %s, %s);"
    d.commit_to_database(sql, data_warehosue)
    d.disconnect_from_database_server()


if __name__ == '__main__':
    main()

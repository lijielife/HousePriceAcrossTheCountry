#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import sys
from multiprocessing.dummy import Pool as ThreadPool

from bs4 import BeautifulSoup

sys.path.append('../')
from tool import mysql

def read_file(filename):
    with open(filename) as fp:
        html = fp.read()
    return html

def read_file_in_multiprocess():
    files_list = glob.glob('anjuke_second_house/*.txt')

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
        loupan_name_detail = information.find(name='div', attrs={'class': 'lp-name'}).find(name='h3').find(name='a')['href']
        # 楼盘状态
        status = [x.get_text().encode('utf8').strip() for x in information.find(name='div', attrs={'class': 'lp-name'}).find_all(name='i')]
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

def anjuke_second_house_data_extract(html):
    temp_list = []
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    for item in soup.find(name='ul', attrs={'class': 'houselist-mod'}).find_all(name='li', attrs={'class': 'list-item'}):
        house_details = item.find(name='div', attrs={'class': 'house-details'})
        house_title = house_details.find(name='div', attrs={'class': 'house-title'}).find(name='a').get_text().strip()
        house_link = house_details.find(name='div', attrs={'class': 'house-title'}).find(name='a')['href']
        details_item_1 = house_details.find_all(name='div', attrs={'class': 'details-item'})[0]
        house_area = details_item_1.find_all(name='span')[0].get_text().strip()
        house_allocation = details_item_1.find_all(name='span')[1].get_text().strip()
        house_per_price = details_item_1.find_all(name='span')[2].get_text().strip()
        details_item_2 = house_details.find_all(name='div', attrs={'class': 'details-item'})[1]
        house_location = details_item_2.find(name='span', attrs={'class': 'comm-address'})['title']
        pro_price = item.find(name='div', attrs={'class': 'pro-price'})
        house_price = pro_price.find(name='span', attrs={'class': 'price-det'}).get_text().strip()
        temp_list.append((house_title, house_link, house_area, house_allocation, house_location, house_per_price,
                          house_price))
    return temp_list

def anjuke_renting_house_data_extract(html):
    temp_list = []
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    for item in soup.find(name='div', attrs={'class': 'list-content'}).find_all(name='div', attrs={'class': 'zu-itemmod'}):
        zu_info = item.find(name='div', attrs={'class': 'zu-info'})
        house_title = zu_info.find(name='h3').find(name='a').get_text().strip()
        house_link = zu_info.find(name='h3').find(name='a')['href']
        details_item = zu_info.find(name='p', attrs={'class': 'tag'}).get_text().strip()
        house_allocation = details_item.split("|")[0]
        house_renting_type = details_item.split("|")[1]
        house_finish_type = details_item.split("|")[2]
        house_floor = details_item.split("|")[3]
        house_location = ' '.join(zu_info.find(name='address').get_text().strip().split())
        zu_side = item.find(name='div', attrs={'class': 'zu-side'})
        house_price = zu_side.find(name='p').get_text().strip()
        temp_list.append((house_title, house_link, house_allocation, house_renting_type, house_finish_type, house_floor,
                          house_location, house_price))
    return temp_list

def anjuke_data_extract_in_multiprocess(option=0):
    html_list = read_file_in_multiprocess()

    pool = ThreadPool(4)
    if option == 0:
        data_list = pool.map(anjuke_new_house_data_extract, html_list)
    elif option == 1:
        data_list = pool.map(anjuke_second_house_data_extract, html_list)
    elif option == 2:
        data_list = pool.map(anjuke_renting_house_data_extract, html_list)
    pool.close()
    pool.join()

    data_warehosue = []
    for data_seg_list in data_list:
        data_warehosue.extend(data_seg_list)
    
    return data_warehosue

def main():
    data_warehosue = anjuke_data_extract_in_multiprocess(1)

    d = mysql.MySQLAPI(username='root', password="yunan0808")
    d.connect_to_database_server()
    d.change_database('AnJuKe')
    d.commit_to_database(data_warehosue, 1)

if __name__ == '__main__':
    main()

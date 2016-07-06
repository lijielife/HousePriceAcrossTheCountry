#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from mysql import MySql
from multiprocessing.dummy import Pool as ThreadPool
import os
import re


def read_file(filename):
    with open('soufangwang_renting_house/'+filename, 'r') as fp:
        html = fp.read()
    return html, ' '.join(re.findall(r'[a-zA-Z]+', filename[:-4]))


def read_file_in_multiprocess():
    files_list = object
    for _, _, files in os.walk('soufangwang_renting_house/'):
        files_list = files
    pool = ThreadPool(4)
    html_list = pool.map(read_file, files_list)
    pool.close()
    pool.join()
    return html_list


def soufangwang_new_house_data_extract(html_list):
    temp_list = []
    soup = BeautifulSoup(html_list[0], 'lxml', from_encoding='utf-8')
    for item in soup.find(name='div', attrs={'class': 'build_list'}).find_all(name='dl'):
        loupan = item.find_all(name='dd')[0].find(name='p', attrs={'class': 'build_name'})
        loupan_name = loupan.find('a').get_text().strip()
        loupan_detail = 'http://' + html_list[1].split()[0][0].lower() + html_list[1].split()[1][0].lower() + \
                        '.sofang.com' + loupan.find('a')['href']
        address = ' '.join(item.find_all(name='dd')[0].find(name='p', attrs={'class': 'finish_data'}).
                           get_text().strip().split())
        price = item.find_all(name='dd')[1].find_all(name='p')[0].get_text().strip()
        temp_list.append((loupan_name, loupan_detail, address, price))
    return temp_list


def soufangwang_second_house_data_extract(html_list):
    temp_list = []
    soup = BeautifulSoup(html_list[0], 'lxml', from_encoding='utf-8')
    for item in soup.find(name='div', attrs={'class': 'build_list'}).find_all(name='dl'):
        loupan = item.find_all(name='dd')[0].find(name='p', attrs={'class': 'build_name'})
        house_title = loupan.find('a').get_text().strip()
        house_link = 'http://' + html_list[1].split()[0][0].lower() + html_list[1].split()[1][0].lower() + \
                     '.sofang.com' + loupan.find('a')['href']
        house_location = ' '.join(item.find_all(name='dd')[0].find(name='p', attrs={'class': 'finish_data'}).
                                  get_text().strip().split())
        house_allocation = item.find_all(name='dd')[0].find(name='p', attrs={'class': 'home_num'}).\
            get_text().strip().split('|')[0].strip()
        house_area = item.find_all(name='dd')[1].find_all(name='p')[0].get_text().strip().split()[0]
        house_per_price = item.find_all(name='dd')[1].find_all(name='p')[1].get_text().strip().strip().split()[1]
        house_price = item.find_all(name='dd')[1].find_all(name='p')[0].get_text().strip().split()[1]
        temp_list.append((house_title, house_link, house_area, house_allocation, house_location, house_per_price,
                          house_price))
    return temp_list


def soufangwang_renting_house_data_extract(html_list):
    temp_list = []
    soup = BeautifulSoup(html_list[0], 'lxml', from_encoding='utf-8')
    for item in soup.find(name='div', attrs={'class': 'build_list'}).find_all(name='dl'):
        loupan = item.find_all(name='dd')[0].find(name='p', attrs={'class': 'build_name'})
        house_title = loupan.find('a').get_text().strip()
        house_link = 'http://' + html_list[1].split()[0][0].lower() + html_list[1].split()[1][0].lower() + \
                     '.sofang.com' + loupan.find('a')['href']
        house_location = ' '.join(item.find_all(name='dd')[0].find(name='p', attrs={'class': 'finish_data'}).
                                  get_text().strip().split())
        house_renting_type = item.find_all(name='dd')[0].find(name='p', attrs={'class': 'home_num'}). \
            get_text().strip().split('|')[0].strip()
        house_floor = item.find_all(name='dd')[0].find(name='p', attrs={'class': 'home_num'}). \
            get_text().strip().split('|')[2].strip()
        house_allocation = item.find_all(name='dd')[1].find_all(name='p')[0].get_text().strip().split()[0]
        house_price = item.find_all(name='dd')[1].find_all(name='p')[0].get_text().strip().split()[1]
        temp_list.append((house_title, house_link, house_allocation, house_renting_type, house_floor, house_location,
                          house_price))
    return temp_list


def soufangwang_data_extract_in_multiprocess():
    html_list = read_file_in_multiprocess()
    pool = ThreadPool(4)
    data_list = pool.map(soufangwang_renting_house_data_extract, html_list)
    pool.close()
    pool.join()
    data_warehosue = []
    for data_seg_list in data_list:
        data_warehosue.extend(data_seg_list)
    return data_warehosue


def main():
    data_warehosue = soufangwang_data_extract_in_multiprocess()
    d = MySql(host='121.42.188.55', port=3306,
              username='root', password='tianchi',
              charset="utf8")
    d.connect_to_database_server()
    d.change_database('SouFangWang')
    # sql = "INSERT INTO SouFangWang_New_House(loupan_name, loupan_name_detail, address, price) VALUES(%s, %s, %s, %s);"
    # sql = "INSERT INTO SouFangWang_Second_House(loupan_name, loupan_name_detail, area, allocation, address, per_price, " \
    #       "price) VALUES(%s, %s, %s, %s, %s, %s, %s);"
    sql = "INSERT INTO SouFangWang_Renting_House(loupan_name, loupan_name_detail, allocation, renting_type, floor, " \
          "address, price) VALUES(%s, %s, %s, %s, %s, %s, %s);"
    d.commit_to_database(sql, data_warehosue)
    d.disconnect_from_database_server()


if __name__ == '__main__':
    main()

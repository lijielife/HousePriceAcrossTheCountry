#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author : Zhou Jian
@email  : summychou@163.com
'''

import csv
import re
import sys

sys.path.append('../')
from tool import mysql

def main():
    d = mysql.MySQLAPI(username='root', password="yunan0808")
    d.connect_to_database_server()
    d.change_database('AnJuKe')

    sql = "SELECT * FROM AnJuKe_New_House WHERE price != '售价待定' AND price LIKE '均价%';"
    results = d.query_from_database_using_sql(sql)
    results = [(result[1].encode('utf8'), result[2].encode('utf8'), result[3].encode('utf8'), re.findall(r'\d+', result[4].encode('utf8'))[0]) for result in results]

    csvfile = file('anjuke_new_house_data/AnJuKe_New_House.csv', 'w')
    writer = csv.writer(csvfile)
    writer.writerow([u'楼盘'.encode('utf8'), u'楼盘链接'.encode('utf8'), u'地理位置'.encode('utf8'), u'价格|元/m2'.encode('utf8')])
    writer.writerows(results)
    csvfile.close()

    sql = "SELECT * FROM AnJuKe_Second_House;"
    results = d.query_from_database_using_sql(sql)
    results = [(result[1].encode('utf8'), result[2].encode('utf8').split('?')[0],
        re.findall(r'\d+', result[3].encode('utf8'))[0], result[4].encode('utf8'),
        result[5].encode('utf8'), re.findall(r'\d+', result[6].encode('utf8'))[0],
        re.findall(r'\d+', result[3].encode('utf8'))[0]) for result in results]

    csvfile = file('anjuke_second_house_data/AnJuKe_Second_House.csv', 'w')
    writer = csv.writer(csvfile)
    writer.writerow([u'宣传标语'.encode('utf8'), u'楼盘链接'.encode('utf8'), u'面积|m2'.encode('utf8'),
        u'房型'.encode('utf8'), u'楼盘描述'.encode('utf8'), u'均价|元/m2'.encode('utf8'), u'总价|万'.encode('utf8'),])
    writer.writerows(results)
    csvfile.close()

if __name__ == '__main__':
    main()

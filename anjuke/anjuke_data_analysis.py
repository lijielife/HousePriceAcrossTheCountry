#!/usr/bin/python
# -*- coding: utf-8 -*-
from mysql import MySql
import re
import xlwt


def main():
    d = MySql(host='121.42.188.55', port=3306,
              username='root', password='tianchi',
              charset="utf8")
    d.connect_to_database_server()
    d.change_database('AnJuKe')
    sql = "SELECT * FROM AnJuKe_New_House WHERE loupan_name_detail LIKE 'http://sz.fang.anjuke.com/loupan/%.html' AND " \
          "price != '售价待定' AND price LIKE '均价%';"
    results = d.query_from_database(sql)
    d.disconnect_from_database_server()

    excel = xlwt.Workbook()
    sheet = excel.add_sheet('DataSheet', cell_overwrite_ok=True)
    for (j, result) in enumerate(results):
        sheet.write(j, 0, result[1])
        sheet.write(j, 1, result[3])
        price = re.findall(r'[0-9]+', result[4])
        sheet.write(j, 2, int(price[0]))
    excel.save("anjuke_new_house_data/ShenZhen_New_House.xls")


if __name__ == '__main__':
    main()

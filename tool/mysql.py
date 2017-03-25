#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author : Zhou Jian
@email  : summychou@163.com
'''

import time
from functools import wraps

try:
    import MySQLdb
except ImportError, e:
    print '>> MySQLdb Module is not found, please install it first'


def customized_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class MySQLAPI(object):

    def __init__(self, username, password, host='localhost', port=3306, charset='utf8'):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._charset = charset
        self._conn = object
        self._db = object
    
    def __del__(self):
        self.__disconnect_from_database_server()

    def __call__(self):
        pass
    
    def __str__(self):
        return '[{}] New MySQL Connection Object [ {}@{}:{} ]'.format(self.__now(), self._username, self._host, self._port)

    def __repr__(self):
        return '[{}] New MySQL Connection Object [ {}@{}:{} ]'.format(self.__now(), self._username, self._host, self._port)

    def connect_to_database_server(self):
        try:
            self._conn = MySQLdb.connect(
                host=self._host, port=self._port,
                user=self._username, passwd=self._password, 
                charset=self._charset)
            print u'[{}] Connected To MySQL Server'.format(self.__now())
        except MySQLdb.OperationalError, e:
            print '[{}] Status Code: {}, Reason: {}'.format(self.__now(), e[0], e[1])
            print u'[{}] Connection Is Failed，Check Your Configuration Information'.format(self.__now(), )

    def change_database(self, db):
        self._conn.select_db(db)
        self._db = db
        print u'[{}] Connected To Database - {}'.format(self.__now(), self._db)

    def commit_to_database(self, data_list, sql_options=0):
        sql, table = self.__sql_options(sql_options)

        cur = self._conn.cursor()
        print u'[{}] Submit {} Data Records Into {}/{} ...'.format(self.__now(), len(data_list), self._db, table)
        try:
            cur.executemany(sql, data_list)
            self._conn.commit()
            print u'[{}] Submit Successfully'.format(self.__now())
        except MySQLdb.ProgrammingError:
            self._conn.rollback()
            print '[{}] Status code: {0}, Reason: {1}'.format(self.__now(), e[0], e[1])
            print u'[{}] Submit Failed'.format(self.__now())
        finally:
            cur.close()

    def query_from_database(self, sql_options=3):
        sql, table = self.__sql_options(sql_options)

        q = []
        cur = self._conn.cursor()
        print u'[{}] Query Data Records From {}/{} ...'.format(self.__now(), self._db, table)
        try:
            cur.execute(sql)
            q = cur.fetchall()
            print u'[{}] Query Successfully'.format(self.__now())
        except MySQLdb.ProgrammingError, e:
            print '[{}] Status code: {0}, Reason: {1}'.format(self.__now(), e[0], e[1])
            print u'[{}] Query Failed'.format(self.__now())
        finally:
            cur.close()
        return q

    def __sql_options(self, sql_options=0):
        sql = ''
        table = ''
        if sql_options == 0:
            sql = 'INSERT INTO {}_New_House(loupan_name, loupan_name_detail, address, price) VALUES(%s, %s, %s, %s);'.format(self._db)
            table = '{}_New_House'.format(self._db)
        elif sql_options == 1:
            sql = 'INSERT INTO {}_Second_House(loupan_name, loupan_name_detail, area, allocation, address, per_price, price)' \
            ' VALUES(%s, %s, %s, %s, %s, %s, %s);'.format(self._db)
            table = '{}_Second_House'.format(self._db)
        elif sql_options == 2:
            sql = 'INSERT INTO {}_Renting_House(loupan_name, loupan_name_detail, allocation, renting_type, finish_type, floor, address, price)' \
            ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s);'.format(self._db)
            table = '{}_Renting_House'.format(self._db)
        elif sql_options == 3:
            sql = 'SELECT * FROM {}_New_House'.format(self._db)
            table = '{}_New_House'.format(self._db)
        elif sql_options == 4:
            sql = 'SELECT * FROM {}_Second_House'.format(self._db)
            table = '{}_Second_House'.format(self._db)
        elif sql_options == 5:
            sql = 'SELECT * FROM {}_Renting_House'.format(self._db)
            table = '{}_Renting_House'.format(self._db)
        return sql, table

    def __disconnect_from_database_server(self):
        self._conn.close()
        print u'[{}] Disconnected from MySQL Server'.format(self.__now())

    @staticmethod
    def __now():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def UnitTest():
    d = MySQLAPI(username='root', password='yunan0808')
    print d
    d.connect_to_database_server()
    d.change_database('AnJuKe')
    queries = d.query_from_database(4)
    for query in queries:
        print query

if __name__ == '__main__':
    UnitTest()

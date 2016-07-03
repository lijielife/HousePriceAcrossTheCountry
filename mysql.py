#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb


class MySql(object):

    def __init__(self, host, port, username, password, charset):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.charset = charset
        self.conn = object

    def connect_to_database_server(self):
        try:
            self.conn = MySQLdb.connect(host=self.host, port=self.port,
                                        passwd=self.password, user=self.username,
                                        charset=self.charset)
            print u'数据库服务器连接成功'
        except MySQLdb.OperationalError, e:
            print 'status code: {0}, reason: {1}'.format(e[0], e[1])
            print u'数据库服务器连接失败，请检查用户信息'

    def change_database(self, db):
        self.conn.select_db(db)
        print u'连接到{0}数据库'.format(db)

    def commit_to_database(self, sql, data_list):
        cur = self.conn.cursor()
        print u'正在提交数据至目标数据表...'
        try:
            cur.executemany(sql, data_list)
            self.conn.commit()
            print u'数据提交完毕'
        except MySQLdb.ProgrammingError:
            self.conn.rollback()
            print u'数据提交'
        finally:
            cur.close()

    def query_from_database(self, sql):
        q = []
        cur = self.conn.cursor()
        print u'正在提取数据表内的目标数据...'
        try:
            cur.execute(sql)
            q = cur.fetchall()
            print u'数据提取完毕'
        except MySQLdb.ProgrammingError, e:
            print 'status code: {0}, reason: {1}'.format(e[0], e[1])
            print u'数据提取失败'
        finally:
            cur.close()
        return q

    def disconnect_from_database_server(self):
        self.conn.close()
        print u'断开与数据库服务器的连接'


if __name__ == '__main__':
    d = MySql(host='localhost', port=3306,
              username='root', password='yunan0808',
              charset="utf8")
    d.connect_to_database_server()
    d.change_database('mysql')
    d.disconnect_from_database_server()

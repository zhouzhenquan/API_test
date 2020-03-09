'''
 @Time    : 2020/2/26 16:39
 @Author  : 周振全
 @File    : Connect_DB.py
 @Software: PyCharm

'''

"""
查询数据库

"""
from decimal import Decimal
import pymysql


class DB():

    # 创建一个连接对象
    # def __init__(self):
    #     self.conn = pymysql.connect(host=conf.get("db","host"),
    #                                 port=conf.getint("db","port"),
    #                                 user=conf.get("db","user"),
    #                                 password=conf.get("db","pwd"),
    #                                 charset = conf.get("db", "charset"),
    #                                 # 控制查询出来的数据类型
    #                                 cursorclass=pymysql.cursors.DictCursor,
    #                                 )

    def __init__(self):
        self.conn = pymysql.connect(host='120.78.128.25',
                                    port=3306,
                                    user='future',
                                    password='123456',
                                    # 控制查询出来的数据类型
                                    cursorclass=pymysql.cursors.DictCursor,
                                    charset='utf8')
        # 创建一个游标
        self.cur = self.conn.cursor()

    # 返回一条数据
    def find_one(self,sql):
        self.conn.commit()
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data

    # 返回多条数据
    def find_all(self,sql):
        self.conn.commit()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    # 返回查数据的条数
    def find_count(self,sql):
        self.conn.commit()
        return self.cur.execute(sql)

    # 关闭游标和断开连接
    def close(self):
        self.cur.close()
        self.conn.close()

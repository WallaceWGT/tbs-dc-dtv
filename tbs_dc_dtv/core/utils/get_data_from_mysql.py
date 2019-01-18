#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

import pymysql
from com.config.service import mysql

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class OperateReportData(object):

    def __init__(self, block_mysql_ele):
        self.block_mysql_ele = block_mysql_ele
        self.mysql_obj = None
        self.mysql_cursor = None
        self.mysql_connect()
        self.sql = self.create_sql()

    # 连接数据库
    def mysql_connect(self):
        self.mysql_obj = pymysql.connect(mysql[1]['host'], mysql[1]['user'], mysql[1]['password'], mysql[1]['database'])
        self.mysql_cursor = self.mysql_obj.cursor()

    # sql语句生成
    def create_sql(self):
        select_ele = ','.join(self.block_mysql_ele['select'])
        from_ele = self.block_mysql_ele['from']
        where = self.block_mysql_ele['where']
        group_by = ','.join(filter(lambda x:x if x != '' else False, self.block_mysql_ele['group_by']))
        order_by = ','.join(filter(lambda x:x if x != '' else False, self.block_mysql_ele['order_by']))
        if self.block_mysql_ele['page'] != 0:
            limit_ele = self.block_mysql_ele['page']*self.block_mysql_ele['page_size'], (self.block_mysql_ele['page']+1)*self.block_mysql_ele['page_size']
        else:
            limit_ele = 0, self.block_mysql_ele['page_size']
        if group_by and order_by:
            sql = "select %s from %s where %s group by %s order by %s limit %s, %s;" % (select_ele, from_ele, where, group_by, order_by, limit_ele[0], limit_ele[1])
        elif not group_by and order_by:
            sql = "select %s from %s where %s order by %s limit %s, %s;" % (select_ele, from_ele, where, order_by, limit_ele[0], limit_ele[1])
        elif group_by and not order_by:
            sql = "select %s from %s where %s group by %s limit %s, %s;" % (select_ele, from_ele, where, group_by, limit_ele[0], limit_ele[1])
        else:
            sql = "select %s from %s where %s limit %s, %s;" % (select_ele, from_ele, where, limit_ele[0], limit_ele[1])
        return sql

    # 执行sql语句生成数据并返回
    def execute_sql(self):
        print self.sql
        self.mysql_cursor.execute(self.sql)
        return self.mysql_cursor.fetchall()

    # 对象查询结束关闭mysql
    def __del__(self):
        self.mysql_cursor.close()
        self.mysql_obj.close()

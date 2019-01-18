#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

import json
from com.utils import MyTime


# 初始化数据时间
def get_init_sql_where(request, block_obj):
    sql_where = ''

    if block_obj.report_type == 1:
        start_date = MyTime.date_to_dt(MyTime.get_date(20))
        end_date = MyTime.date_to_dt(MyTime.get_date(0))
    # 周报
    elif block_obj.report_type == 2:
        start_date, end_date = MyTime.get_week2(MyTime.get_date(180), MyTime.get_date(0))
        start_date = MyTime.date_to_dt(start_date)
        end_date = MyTime.date_to_dt(end_date)
    # 月报
    elif block_obj.report_type == 3:
        start_date, end_date = MyTime.get_month2(MyTime.get_date(360), MyTime.get_date(0))
        start_date = MyTime.date_to_dt(start_date)
        end_date = MyTime.date_to_dt(end_date)
    # 年报
    elif block_obj.report_type == 4:
        start_date = '20090101'
        end_date = MyTime.date_to_dt(MyTime.get_date(0))
    elif block_obj.report_type == 5:
        start_date = None
        end_date = None
    else:
        start_date = MyTime.date_to_dt(MyTime.get_date(360))
        end_date = MyTime.date_to_dt(MyTime.get_date(0))

    if start_date:
        sql_where = "stat_date between %s and %s" % (start_date, end_date)
    return sql_where


# 图表, 表格
def get_date_change_sql_where(request, block_obj):
    sql_where = None
    # 对于表格来说：今天, 昨天, 最近7天, 最近30天, 上翻, 下翻

    # 对于图表来说：日报, 周报, 月报, 年报： 起始月份
    # 从那一天开始: 到那一天结束, 若没有传入结束日期, 则默认是后30个数据
    if block_obj == 0:
        start_date = MyTime.date_to_dt(request.GET.get('start_date'))
        if request.GET.get('end_date'):
            end_date = request.GET.get('end_date')
        else:
            end_date = MyTime.date_to_dt(MyTime.get_date(0))
    elif block_obj == 1:
        if request.GET.get('get_today'):
            start_date = MyTime.date_to_dt(MyTime.get_date(0))
            end_date = MyTime.date_to_dt(MyTime.get_date(0))
        elif request.GET.get('get_yesterday'):
            start_date = MyTime.date_to_dt(MyTime.get_date(1))
            end_date = MyTime.date_to_dt(MyTime.get_date(0))
        elif request.GET.get('get_7_day'):
            start_date = MyTime.date_to_dt(MyTime.get_date(7))
            end_date = MyTime.date_to_dt(MyTime.get_date(0))
        elif request.GET.get('get_30_today'):
            start_date = MyTime.date_to_dt(MyTime.get_date(30))
            end_date = MyTime.date_to_dt(MyTime.get_date(0))
        else:
            start_date = MyTime.date_to_dt(MyTime.get_date(30))
            end_date = MyTime.date_to_dt(MyTime.get_date(0))
    else:
        start_date = None
        end_date = None

    if start_date:
        sql_where = "stat_date between %s and %s" % (start_date, end_date)

    return sql_where


# 获取
def get_query_sql_where(request, block_obj):
    sql_where = get_init_sql_where(request, block_obj)
    print request.GET.get('query')
    if request.GET.get('query') == 'false':
        return sql_where
    else:
        query_fields = json.loads(request.GET.get('query'))
        sql_where = ''
        if 'start_date' in query_fields.keys():
            sql_where += get_date_change_sql_where(request, block_obj)
        else:
            sql_where += get_init_sql_where(request, block_obj)
        for i in query_fields.keys():
            if i == 'start_date':
                continue
            else:
                sql_where += "and %s=%s" % (i, query_fields[i])
        return sql_where





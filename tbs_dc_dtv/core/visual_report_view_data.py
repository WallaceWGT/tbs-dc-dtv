#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

import json
from com.utils import MyTime
from tbs_dc_dtv.libs.display import models
from tbs_dc_dtv.core.utils import get_data_from_mysql
from tbs_dc_dtv.core.utils import get_query_sql
import decimal
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_visual_report_block_data(request):
    return_data = {'code': 0, 'message': 'success', 'data': {}}
    block_id = request.GET.get('bid')
    block_obj = models.BdpDataVisualBlockConfig.objects.filter(bid=block_id)[0]

    block_ele = {'from': block_obj.source_name, 'where': '', 'group_by': [], 'select': [], 'order_by': [],
                 'columns': [], 'columns_cn': [], 'page': None, 'page_size': 29}

    method_ini = {0: "sum(%s)", 1: "count(%s)", 2: "min(%s)", 3: "max(%s)", 4: "avg(%s)"}
    order_ini = {0: '', 1: "desc", 2: "asc"}
    all_field_ele = models.BdpDataVisualBlockField.objects.values().filter(bid=block_id).order_by('fid')

    # 条件过滤
    if request.GET.get('query'):
        sql_where = get_query_sql.get_query_sql_where(request, block_obj)
    # 无过滤条件则进行数据的初始化数据
    else:
        sql_where = get_query_sql.get_init_sql_where(request, block_obj)
    if sql_where:
        block_ele['where'] = sql_where
    if block_obj.source_filter != '':
        block_ele['where'] += "and %s" % block_obj.source_filter

    # 字段sql组成
    for j in all_field_ele:
        if j['formula'] != '' and j['formula'] is not None:
            select_ele = j['formula']
        elif j['method'] is not None:
            select_ele = method_ini[j['method']] % j['field_name']
        else:
            # 没有公式的一般都是维度信息
            select_ele = j['field_name']

        # order_by 字段判断
        order_ele = order_ini[j['is_sort']]
        if order_ele != '':
            order_ele = j['field_name'] + " " + order_ele

        # group by 判断
        if j['furl_mode'] is None or j['field_type'] == 0:
            group_by_ele = ''
        else:
            group_by_ele = j['field_name']
        if j['field_type'] != 0:
            block_ele['select'].insert(0, select_ele)
            block_ele['columns'].insert(0, j['field_name'])
            block_ele['columns_cn'].insert(0, j['field_name_cn'])
        else:
            block_ele['select'].append(select_ele)
            block_ele['columns'].append(j['field_name'])
            block_ele['columns_cn'].append(j['field_name_cn'])
        block_ele['order_by'].append(order_ele)
        block_ele['group_by'].append(group_by_ele)

    # 数据显示个数, 默认显示30个
    if request.GET.get("page"):
        page = request.GET.get("page")
    else:
        page = 0
    block_ele['page'] = page

    # 执行sql, 得到数据并进行返回
    mysql_operate_obj = get_data_from_mysql.OperateReportData(block_ele)
    block_data = mysql_operate_obj.execute_sql()

    # 对返回的数据进行处理
    deal_block_data = []
    for single_block_data in block_data:
        # mysql 获取的有些数据是decimal.Decimal类型的数据, 需要将其转换成普通的字符串形式
        j = map(lambda x: str(x.quantize(decimal.Decimal('0'))) if isinstance(x, decimal.Decimal) else x,
                single_block_data)
        deal_block_data.append(j)
    if block_obj.block_type == 0:
        return_data['data']['chart_type'] = block_obj.chart_type
    return_data['data']['field_data'] = deal_block_data
    return_data['data']['columns_cn'] = block_ele['columns_cn']
    return_data['data']['columns'] = block_ele['columns']
    return_data['data']['block_type'] = block_obj.block_type

    return return_data



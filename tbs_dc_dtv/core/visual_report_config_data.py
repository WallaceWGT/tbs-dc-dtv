#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

import json
import pymysql
from com.config.service import mysql
from django.http import QueryDict
from tbs_dc_dtv.libs.display import models


# 用于处理报表配置的块数据配置时进行存储或更新
def visual_report_block_update_or_create(request):
    for i in json.loads(request.POST.get('data')):
        # 判断是是否是已经存在的内容块，如果不存在则bid为None
        try:
            bid = json.loads(i)['bid']
        except KeyError:
            bid = None

        # 初始化没一块的基础数据，方便对不同块的数据进行存储
        block_data = {'vid': None, 'block_type': None, 'region_id': None, 'block_name': None,
                      'chart_type': None, 'source_name': None, 'report_type': None,  'block_content': None}

        # 对每一块进行赋值, 若某数据块不存在某个key对应的指，则跳过
        for key in block_data.keys():
            try:
                block_data[key] = json.loads(i)[key]
            except KeyError:
                continue

        # 将每一块的数据进行存储
        visual_obj = models.BdpDataVisualReport.objects.filter(vid=block_data['vid'])
        block_data['vid'] = visual_obj[0]

        if bid is None:
            models.BdpDataVisualBlockConfig.objects.create(**block_data)
        else:
            block_data['bid'] = bid
            models.BdpDataVisualBlockConfig.objects.filter(bid=bid).update(**block_data)

        # 获取每一个数据块对象，用于对每一块的指标进行存储
        if bid is None:
            block_obj = models.BdpDataVisualBlockConfig.objects.filter(block_name=block_data['block_name'],
                                                                       vid=block_data['vid'])[0]
        else:
            block_obj = models.BdpDataVisualBlockConfig.objects.filter(bid=bid)[0]

        # 有些内容没有指标，就不进行指标初始化, 直接跳过
        if str(json.loads(i)['block_type']) == "2":
            continue
        else:
            all_fields = {'field_name': None, 'field_name_cn': None, 'field_type': None, 'method': None,
                          'formula': None, 'fid': None, 'is_sort': None, 'furl_mode': None, 'is_filter': None, 'is_show': None}

        for key2 in all_fields.keys():
            try:
                all_fields[key2] = json.loads(i, encoding='utf-8')[key2].split('-')
            except KeyError, e:
                all_fields[key2] = []

        # 因为指标和维度字段的值不同, 所以在对应索引位置上用None进行替代
        for i in all_fields['field_type']:
            ele_index = all_fields['field_type'].index(i)
            if i != '0':
                all_fields['formula'].insert(ele_index, '')
                all_fields['method'].insert(ele_index, None)
            else:
                all_fields['furl_mode'].insert(ele_index, 0)
        print all_fields
        # 初始化完毕, 进行数据存储
        for j in range(len(all_fields['field_name'])):
            field_data = {'field_name': None, 'field_name_cn': None, 'field_type': None,  'method': None,
                          'formula': None, 'fid': None, 'is_sort': None, 'furl_mode': 0, 'is_filter': None, 'is_show': None}

            for key3 in field_data.keys():
                field_data[key3] = all_fields[key3][j]
                field_data['bid'] = block_obj
            if field_data['fid']:
                models.BdpDataVisualBlockField.objects.filter(fid=field_data['fid']).update(**field_data)
            else:
                del field_data['fid']
                models.BdpDataVisualBlockField.objects.create(**field_data)
    return {"code": 0, "message": "success", "data": None}


# 数据块指标删除或维度
def visual_report_block_or_field_delete(request):
    del_info = QueryDict(request.body)
    if del_info.get("fid"):
        fid = del_info.get('fid')
        models.BdpDataVisualBlockField.objects.filter(fid=fid).delete()
    elif del_info.get("bid"):
        bid = del_info.get("bid")
        models.BdpDataVisualBlockConfig.objects.filter(bid=bid).delete()
    return {"code": 0, "message": "success", "data": None}


# 获取报表数据字段的值,判断是否为指标还是维度
def get_report_table_field_info(request):
    table_info = QueryDict(request.body)
    table_name = table_info.get("table_name")
    data_type = {}
    mysql_obj = pymysql.connect(mysql[1]['host'], mysql[1]['user'], mysql[1]['password'], mysql[1]['database'])
    mysql_cursor = mysql_obj.cursor()

    # 获取对应数据表的字段,以及字段所需的数据类型
    try:
        mysql_cursor.execute("select COLUMN_NAME,DATA_TYPE from information_schema.COLUMNS "
                    "where table_name = %s and table_schema = 'tbs_dc_rep';", table_name)
    except Exception as e:
        return {"code": 90011, "message": str(e), "data": ""}
    field_info_data = mysql_cursor.fetchall()
    mysql_obj.close()
    for single_field in field_info_data:
        if single_field[0] == "stat_date":
            data_type[single_field[0]] = "dimension"
        elif single_field[1] == "varchar" or single_field[1] == "text":
            data_type[single_field[0]] = "dimension"
        else:
            data_type[single_field[0]] = "quota"
    return {"code": 0, "message": "success", "data": json.dumps(data_type)}

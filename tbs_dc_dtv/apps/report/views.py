# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import time
import json

reload(sys)
sys.setdefaultencoding("utf8")
from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from forms import ReportMenuForm
from forms import VisualReportForm
from tbs_dc_dtv.libs.display import models
from tbs_dc_dtv.core.visual_report_config_data import visual_report_block_update_or_create
from tbs_dc_dtv.core.visual_report_config_data import visual_report_block_or_field_delete
from tbs_dc_dtv.core.visual_report_config_data import get_report_table_field_info
from tbs_dc_dtv.core.visual_report_view_data import get_visual_report_block_data


# 菜单配置
@method_decorator(csrf_exempt)
def visual_report_menu_setting(request):
    if request.method == 'GET':
        menu_form = ReportMenuForm()
    else:
        menu_form = ReportMenuForm(request.POST)
        if menu_form.is_valid():
            menu_name = menu_form.cleaned_data['menu_name']
            models.BdpDataVisualMenu.objects.update_or_create(
                menu_name=menu_name,
                create_uid=1,
                create_time=time.time(),
                update_time=time.time(),
                update_uid=1
            )
        return redirect('/visual/report_view')
    return render(request, 'report/report_menu_config.html', {'menu_form': menu_form})


@method_decorator(csrf_exempt)
def visual_report_view(request):
    if request.method == "GET":
        if request.GET.get('init') or request.GET.get('query') or request.GET.get('start_time'):
            data = get_visual_report_block_data(request)
            return HttpResponse(json.dumps(data))
        else:
            vid = request.GET.get('vid')
            block_objs = models.BdpDataVisualBlockConfig.objects.filter(vid_id=vid).order_by("region_id")
            return render(request, 'report/report_view.html', {'block_objs': block_objs})
    else:
        return render(request, 'report/report_view.html')


# 数据报表配置
@method_decorator(csrf_exempt)
def visual_report_setting(request):
    if request.method == "GET":
        report_form_obj = VisualReportForm()
        return render(request, 'report/report_config.html', {'report_form_obj': report_form_obj})
    else:
        return redirect('/visual/report_view')


# 数据报表详情信息配置
@method_decorator(csrf_exempt)
def visual_report_block_config(request):
    """
    可视化报表块配置
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 更加对应的报表id返回数据库已经存在的数据块对象以及对应的指标
        vid = request.GET.get('vid')
        block_obj = models.BdpDataVisualBlockConfig.objects.filter(vid=vid).order_by('region_id')
        filed_obj = models.BdpDataVisualBlockField.objects.filter(bid__vid=vid)
        return render(request, 'report/report_block_config.html', {'block_obj': block_obj, 'field_obj': filed_obj})
    elif request.method == "POST":
        response = visual_report_block_update_or_create(request)
        return HttpResponse(json.dumps(response))
    elif request.method == "DELETE":
        response = visual_report_block_or_field_delete(request)
        return HttpResponse(json.dumps(response))
    elif request.method == "PUT":
        response = get_report_table_field_info(request)
        return HttpResponse(json.dumps(response))


# 登入
def visual_login(request):
    pass


# 注销
def visual_logout(request):
    pass


# 主页
def home_page(request):
    pass


def test(request):
    if request.method == 'GET':
        if request.GET.get('query'):
            print json.loads(request.GET.get('query'))
        else:
            print 'fasdf'
        return  render(request, 'public/test.html')



"""
查询逻辑是一致的：

"""
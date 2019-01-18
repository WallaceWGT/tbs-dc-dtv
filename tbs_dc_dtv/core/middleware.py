#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

"""
该文档用于创建该项目的中间件，用于扩展在请求到来之前和请求结束返回时进行一些操作
"""

from django.utils.deprecation import MiddlewareMixin
from tbs_dc_dtv.libs.display import models


class ReportMenu(MiddlewareMixin):
    """
    改模块的功能就是在请求到来之后给request添加报表菜单的属性
    方便前端进行菜单数据的获取
    """
    def process_request(self, request):
        request.report_menu = models.BdpDataVisualMenu.objects.all()

    def process_response(self, request, response):
        return response
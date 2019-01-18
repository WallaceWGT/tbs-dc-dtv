#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang
from django.conf.urls import url

from tbs_dc_dtv.apps.report import views

urlpatterns = [
    url(r'report_menu_setting/', views.visual_report_menu_setting),
    url(r'report_view', views.visual_report_view),
    url(r'report_setting', views.visual_report_setting),
    url(r'report_block_config', views.visual_report_block_config),
    url(r'test', views.test)
]
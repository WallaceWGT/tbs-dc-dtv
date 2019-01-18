#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_report_title(menu_obj):
    field_names = menu_obj.bdpdatavisualreport_set.all()

    return field_names


@register.simple_tag
def list_all_block(block_obj, field_obj):
    for i in block_obj:
        if i.block_type == "0":
            pass
        elif i.block_type == "1":
            pass
        elif i.block_type == "2":
            pass
        elif i.block_type == "3":
            pass





#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
html生成工具

"""
import os
import datetime
from mako.template import Template
from mako.lookup import TemplateLookup
from webspider.utils.get_project_setting import get_project_setting



def data2html(template_file,**kwargs):
    """数据转换成html"""
    directory = os.path.join(get_project_setting()['SPIDERPATH'],'template')
    date = datetime.date.today().strftime("%Y-%m-%d")
    mlookup = TemplateLookup(directories=[directory],
                             input_encoding='utf-8',
                             output_encoding='utf-8',
                             encoding_errors='replace')
    t = mlookup.get_template(template_file)
    html = t.render(date=date, **kwargs)
    return html

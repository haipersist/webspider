#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
html生成工具

"""
import os
import datetime
from mako.template import Template
from mako.lookup import TemplateLookup



def data2html(data_list, template_file):
    """数据转换成html"""
    directory = os.path.join(os.environ.get('SPIDERPATH'),'template')
    date = datetime.date.today().strftime("%Y-%m-%d")
    mlookup = TemplateLookup(directories=[directory],
                             input_encoding='utf-8',
                             output_encoding='utf-8',
                             encoding_errors='replace')
    t = mlookup.get_template(template_file)
    html = t.render(date=date, data_list=data_list)
    return html


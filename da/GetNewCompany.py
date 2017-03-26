#!/usr/bin/python
#-*-coding:utf-8 -*-

"""
It is used to get the new company.
the serid time may be one day,week or month.
set the date by you.

Usage:
    company = NewCompany()
    dailycom = company.get_daily_company()

"""

from datetime import date
from webspider.baseclass.baseRedis import BaseRedis
from webspider.baseclass.database import Database
from webspider.utils.get_project_setting import get_project_setting


class NewCompany(object):

    def __init__(self):
        self.db = Database()
    @property
    def daily_new_company(self):
        #redis = BaseRedis()
        #return redis.get('new_company',type='list')
        sql = 'select name,address,introduction from company where id>738'
        return self.db.query(sql)

    def get_weekly_company(self):
        pass

    def get_monthly_company(self):
        pass


def load_online_company():
    import requests
    setting = get_project_setting()
    auth = setting['AUTH']
    companies = NewCompany().daily_new_company
    for item in companies:
        try:
            r = requests.post('http://dailyblog.applinzi.com/api/companies/',
                              data=item,
                              auth=auth)
        except Exception, e:
            print str(e)
            continue







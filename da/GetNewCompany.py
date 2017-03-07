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


class NewCompany(object):

    def get_daily_company(self):
        redis = BaseRedis()
        return redis.get('new_company',type='list')

    def get_weekly_company(self):
        pass

    def get_monthly_company(self):
        pass










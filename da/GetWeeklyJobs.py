#!/usr/bin/python
#-*-coding:utf-8 -*-

"""
It is used to get the detail and total number weekly job.
By default,the target date is cur day.of course,you can
set the date by you.
Usage:
    job = WeeklyJob()
    detailjobs =  job.get_week_job()
    total= job.total

"""
import cPickle
from datetime import date,timedelta
from webspider.baseclass.baseRedis import BaseRedis
from webspider.baseclass.database import Database




def query_decorator(method):
    def wrapper(start=None,end=None):
        today = date.today()
        if start is None:
            start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        if end is None:
            end = today.strftime("%Y-%m-%d")
        method(start,end)
    return wrapper



class WeeklyJob(object):

    def __init__(self,day=None):
        self.db = Database()
        self.today = date.today()
        self.start = self.today - timedelta(days=7)
        self.day = self.today if day is None else day

    @query_decorator
    def get_week_job(self,start,end):
        sql = 'select * from jobs where pub_time BETWEEN "%s" and "%s"' % (start,end)
        return self.db.query(sql)

    @query_decorator
    def get_week_total(self,start,end=None):
        sql = 'select count(id) as total from jobs where pub_time BETWEEN "%s" and "%s"' % (start,end)
        count = self.db.query(sql)[0]['total']
        if not isinstance(count, int):
            count = int(count)
        return count






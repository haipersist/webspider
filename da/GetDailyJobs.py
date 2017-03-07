#!/usr/bin/python
#-*-coding:utf-8 -*-

"""
It is used to get the detail and total number daily job.
By default,the target date is cur day.of course,you can
set the date by you.
Usage:
    job = DailyJob()
    detailjobs =  job.get_daily_job()
    total= job.total

"""

from datetime import date
from webspider.baseclass.baseRedis import BaseRedis
from webspider.baseclass.database import Database


class DailyJob(object):

    def __init__(self,day=None):
        self.db = Database()
        self.redis = BaseRedis()
        self.day = date.today().strftime("%Y-%m-%d") if day is None else day

    def get_daily_job(self):
        sql = 'select * from jobs where pub_time="%s"'%self.day
        return self.db.query(sql)

    @property
    def total(self):
        """
        if the day is cur day,it will get data from redis ,or else,
        it will get data from Mysql.Because Redis server only store
        the latest data.
        :return:
        """
        today = date.today().strftime("%Y-%m-%d")
        if cmp(today,self.day) == 0:
            return self.redis.rs.llen('latest_jobs')
        else:
            sql = 'select count(id) as total from jobs where pub_time="%s"' % self.day
            count = self.db.query(sql)[0]['total']
            if not isinstance(count,int):
                count = int(count)
            return count










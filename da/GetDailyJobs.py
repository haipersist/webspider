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
import cPickle
from datetime import date
from webspider.baseclass.baseRedis import BaseRedis
from webspider.baseclass.database import Database


class DailyJob(object):

    def __init__(self,day=None):
        self.db = Database()
        self.redis = BaseRedis()
        self.today = date.today().strftime("%Y-%m-%d")
        self.day = self.today if day is None else day

    def get_daily_job(self):
        #if cmp(self.today,self.day) == 0:
        #    result = self.redis.get('latest_jobs',type='list')
        #    if result:
        #        return [cPickle.loads(item) for item in result]
        sql = 'select * from jobs where pub_time>="%s 00:00:00"'%self.day
        return self.db.query(sql)

    @property
    def total(self):
        """
        if the day is cur day,it will get data from redis ,or else,
        it will get data from Mysql.Because Redis server only store
        the latest data.
        :return:
        """
        if cmp(self.today,self.day) == 0:
            count = self.redis.rs.llen('latest_jobs')
            if count != 0:
                return count
        sql = 'select count(id) as total from jobs where pub_time="%s"' % self.day
        count = self.db.query(sql)[0]['total']
        if not isinstance(count,int):
            count = int(count)
        return count










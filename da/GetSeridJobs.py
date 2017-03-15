#!/usr/bin/python
#-*-coding:utf-8 -*-

"""
It is used to get the detail and total number weekly job.
By default,the target date is cur day.of course,you can
set the date by you.
Usage:
    job = SeridJob()
    detailjobs =  job.get_week_job()
    total= job.total

"""
import cPickle
from datetime import date,timedelta,datetime
from webspider.baseclass.database import Database





class SeridJob(object):

    def __init__(self,end=None,serid=7):
        self.db = Database()
        if end is None:
            self.end = date.today().strftime("%Y-%m-%d")
        else:
            self.end = end
        self.start = (datetime.strptime(self.end,"%Y-%m-%d") - timedelta(days=serid)).strftime("%Y-%m-%d")

    def get_serid_job(self):
        sql = 'select * from jobs where pub_time BETWEEN "%s" and "%s"' % (self.start,self.end)
        return self.db.query(sql)

    def get_serid_total(self):
        sql = 'select count(id) as total from jobs where pub_time BETWEEN "%s" and "%s"' % (self.start,self.end)
        count = self.db.query(sql)[0]['total']
        if not isinstance(count, int):
            count = int(count)
        return count

    def get_serid_job_groupby(self,category):
        sql = 'select category,count(id) as num from jobs GROUP BY %s' % category
        count = self.db.query(sql)
        return count








if __name__ == "__main__":
    day = "2017-01-02"
    import time
    print datetime.strptime(day,"%Y-%m-%d") - timedelta(days=1)
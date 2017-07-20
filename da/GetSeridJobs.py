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
from da import BaseJob




class SeridJob(BaseJob):

    def __init__(self,end=None,serid=7):
        if end is None:
            self.end = date.today().strftime("%Y-%m-%d")
        else:
            self.end = end
        self.start = (datetime.strptime(self.end,"%Y-%m-%d") - timedelta(days=serid)).strftime("%Y-%m-%d")
        super(SeridJob,self).__init__()

    def get_serid_job(self):
        sql = "select * from jobs where date_format(load_time,'%Y-%m-%d') BETWEEN '%s' and '%s'" % (self.start,self.end)
        return self.db.query(sql)

    def get_serid_total(self):
        sql = "select count(id) as total from jobs where date_format(load_time,'%Y-%m-%d') BETWEEN '%s' and '%s'" % (self.start,self.end)
        count = self.db.query(sql)[0]['total']
        if not isinstance(count, int):
            count = int(count)
        return count

    def get_serid_job_groupby(self,category,start=None,end=None):
        where = "where a.pub_time between '%s' and '%s'" % (start,end) \
            if start is not None and end is not None else ''
        if category=='website':
            if not where:
                sql = "select count(a.id) as num,b.website as %s from jobs a join website b " \
                      "on a.website_id=b.id group by a.website_id" % category
            else:
                sql = "select count(a.id) as num,b.website as %s from jobs a join website b " \
                      "on a.website_id=b.id %s group by a.website_id" % (category,where)
        elif category == 'company':
            if not where:
                sql = "select count(a.id) as num,b.name as %s from jobs a join company b " \
                    "on a.company_id=b.id group by a.company_id" % category
            else:
                sql = "select count(a.id) as num,b.name as %s from jobs a join company b " \
                    "on a.company_id=b.id %s group by a.company_id" % (category, where)
        else:
            if category == 'load_time':
                category = 'date_format(%s,'%category+'"%Y-%m-%d")'
            sql = 'select %s,count(id) as num from jobs GROUP BY %s'%(category,category)
        result = self.db.query(sql)
        data = {}
        for item in result:
            data.setdefault(item[category],item['num'])
        return data









if __name__ == "__main__":
    serid = SeridJob()
    result = serid.get_serid_job_groupby('company',
                                         start='2017-06-01 00:00:00',
                                         end='2017-07-20 20:00:00')
    for item in result.keys():
        if result[item]:
            print item,result[item]



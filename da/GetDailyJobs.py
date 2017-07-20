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
from webspider.utils.get_project_setting import get_project_setting
from utils.mylogger import MyLogger
from da import BaseJob


class DailyJob(BaseJob):

    def __init__(self,day=None):
        self.today = date.today().strftime("%Y-%m-%d")
        self.day = self.today if day is None else day
        super(DailyJob,self).__init__()

    def get_daily_job(self):
        if cmp(self.today,self.day) == 0:
            try:
                self.redis = BaseRedis()
                result = self.redis.get('latest_jobs',type='list')
                if result:
		    print 'it comes from redis'
                    return [cPickle.loads(item) for item in result]
            except Exception,e:
                self.logger.error(str(e))

        sql = "select * from jobs where date_format(load_time,'%Y-%m-%d')="+"'%s'"%self.day
        return self.db.query(sql)

    @property
    def total(self):
        """
        if the day is cur day,it will get data from redis ,or else,
        it will get data from Mysql.Because Redis server only store
        the latest data.
        :return:
        """
        sql = "select count(id) as total from jobs where date_format(load_time,'%Y-%m-%d')="+"'%s'" % self.day
        count = self.db.query(sql)[0]['total']
        if not isinstance(count,int):
            count = int(count)
        return count



def load_online_job(day=date.today().strftime("%Y-%m-%d")):
    import requests
    logger = MyLogger('spider').logger
    job = DailyJob(day=day)
    result = job.get_daily_job()
    setting = get_project_setting()
    auth = setting['AUTH']
    for item in result:
        item.pop("id")
        item['pub_time'] = item['pub_time'].strftime("%Y-%m-%d") \
            if item['pub_time'] is not None else day
        item['website'] = item['website_id']
        item.pop("website_id")
        item['company'] = item['company_id']
        item.pop('company_id')
        item.pop('load_time')
        try:
            r = requests.post('http://dailyblog.applinzi.com/api/jobs/',
                              data=item,
                              auth=auth)
        except Exception, e:
            logger.error('Load2line:{0}:{1}:{2}'.format(item['title'],item['link'],str(e)))
            continue





if __name__ == "__main__":
    g = DailyJob()
    print len(g.get_daily_job())

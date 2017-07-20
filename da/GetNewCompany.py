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
import cPickle
from datetime import date
from webspider.baseclass.baseRedis import BaseRedis
from webspider.baseclass.database import Database
from webspider.utils.get_project_setting import get_project_setting
from da import BaseJob

class NewCompany(BaseJob):

    def __init__(self):
        super(NewCompany,self).__init__()

    @property
    def daily_new_company(self):
        try:
            redis = BaseRedis()
            companies = redis.get('new_company',type='list')
            if companies:
                if len(companies) != 0:
		    print 'it comes from redis'
                    return [cPickle.loads(x) for x in companies]
        except Exception,e:
            self.logger.error(str(e))

        sql = 'select name,address,introduction,homepage from company where id>1420'
        return self.db.query(sql)





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
            if r.status_code != 200:
                print item
                print r.text
        except Exception, e:
            print str(e)
            continue



if __name__ == "__main__":
    new = NewCompany()
    print len(new.daily_new_company)



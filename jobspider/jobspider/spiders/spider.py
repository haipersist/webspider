#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
run spider in two different ways

it can run in single spider ,selected from BYR,Lagou,Zhilian,51Job or
run in multiprocessing


Default,the data that spider crawls will be stored into json file ,of course,you can
store into MySQL,excel or redis by setting store type.

"""

import os
from byr import BYR_Spider
from lagou import LG_Spider
from zhilian import ZL_Spider
from job51 import Job51_Spider
from dajie import DJ_Spider
from hbnnwebsite.datasource.jobspider.baseclass.utils.store_data import Job_Data




class Spider():

    spiders = {
        'byr':BYR_Spider('byr','X-Requested-With','Host','Referer'),
        'lagou':LG_Spider('lagou','Host','Cookie'),
        'zhilian':ZL_Spider('zhilian'),
        '51job':Job51_Spider('51job','Host','Cookie'),
        'dajie':DJ_Spider('dajie','X-Requested-With','Host','Referer','Cookie')
               }

    def __init__(self,keyword,store_type='json'):
        self.keyword = keyword
        self.store_type = store_type

    def get_single_data(self,spiname):
        self.spider = self.spiders[spiname]
        data = self.spider.pages_parse(self.keyword)
        return data

    def single_run(self,spiname):
        db = Job_Data(self.store_type)
        for data in self.get_single_data(spiname):
            db.store(data)

    def print_output(self,spiname):
        #In Linux,it will print data with colored
        for data in self.get_single_data(spiname):
            for item in data:
                for key,value in item.items():
                    if not isinstance(key,unicode):
                        key = key.encode('utf8')
                    if not isinstance(value,unicode):
                        value = value.encode('utf8')
                    if os.name == 'posix':
                        try:
                            print '{0}:{1}'.format(red(key),value),
                        except UnicodeEncodeError :
                            key,value = key.encode('utf8'),value.encode('utf8')
                            print '{0}:{1}'.format(key,value)
                        else:
                            print '{0}:{1}'.format(key,value),
                    else:
                        try:
                            print '{0}:{1}'.format(key,value),
                        except UnicodeEncodeError :
                            key,value = key.encode('utf8'),value.encode('utf8')
                            print '{0}:{1}'.format(key,value)
                print '\n'

    def get_data(self,spiname):
        select = raw_input('you want put data into terminal or json(write ter or json):')
        if select == 'terminal':
            self.print_output(spiname)
        elif select == 'json':
            self.single_run(spiname)
        else:
            print 'your input is incorrect,it must be terminal or json'

    def multi_run(self,spiname):
        print spiname
        self.single_run(spiname)







if __name__=="__main__":
    spider = Spider('python')
    spider.get_data('dajie')





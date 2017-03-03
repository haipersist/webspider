# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import requests
import datetime
from webspider.spider.jobspider.items import JobItem,CompanyItem
from webspider.baseclass.database import Database
from webspider.baseclass.baseRedis import BaseRedis
from webspider.utils.mylogger import MyLogger




def dict_decorator(method):
    def to_dict(decorated_instance, item,spider):
        result = {}
        for key in item:
            result[key] = item[key]
            if isinstance(item[key], CompanyItem):
                company = {}
                for ele in result[key]:
                    company[ele] = result[key][ele]
                result[key] = company
        method(decorated_instance,result,spider)

    return to_dict





class MySQLLoadPipeLine(object):

    def __init__(self):
        self.day = datetime.date.today()
        self.year,self.month = str(self.day.year),str(self.day.month)
        self.today = self.day.strftime("%Y-%m-%d")
        self.logger = MyLogger('spider').logger

    @dict_decorator
    def process_item(self, item, spider):
        """
        the method is mainly stores item data into mysql databases
        :param item:#the item is gotten from spiders,item may
        be JobItem or CompanyItem.
        when item is instance of CompanyItem,it will check if the company
        has exsited in database,if not,insert the item into db.As well as
        JobItem,if the job link has exsited in db(link is unique),return.if not
        ,it will insert job info into table:jobs.


        :param spider:
        :return:
        """
        db = Database()
        print item
        sql = 'select id from jobs where link="%s"'%item['link']
        if not db.query(sql):
            company = item['company']
            sql = 'select id,name from company where name="%s"'%company['name']
            if not db.query(sql):
                db.insert_by_dic('company',company)
                self.logger.info(' '.join([company['name'],u'Insert Success!']))
            sql = 'select id from company where name="%s"'%company['name']
            company = db.query(sql)[0]
            try:
                item['company_id'] = company['id']
                item.pop('company')
                db.insert_by_dic('jobs',item)
                self.logger.info(' '.join([item['title'], u'Insert Success!']))
            except IndexError:
                self.logger.error(u'%s::公司名称:%s没有正确添加。请检查.\n' % (self.today,result['company_name']))

        return item



class LoadOnlinePipeline(object):

    def __init__(self):
        self.day = datetime.date.today().strftime("%Y-%m-%d")
        #self.file = codecs.open('store_%s.html'%self.day,'w',encoding='utf8')
        
    @dict_decorator
    def process_item(self, item, spider):
        #line = json.dumps(result,ensure_ascii=False) + "\n"
        #self.file.write(line)
        auth = ('haibo_persist','******')
        r = requests.post('http://dailyblog.applinzi.com/api/onlines/',data=result, auth=auth)
        return item

    def close_spider(self,spider):
        #when the spider is closed ,the method will be called
        #self.file.close()
        pass



class RedisLoadPipeLine(object):
    def __init__(self):
        self.day = datetime.date.today().strftime("%Y-%m-%d")
        # self.file = codecs.open('store_%s.html'%self.day,'w',encoding='utf8')

    @dict_decorator
    def process_item(self, item, spider):
        redis = BaseRedis()
        redis.rs.delete('latest_jobs')
        if item['pub_time'] == self.day:
            redis.set('latest_jobs',[item,0])



# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import cPickle
import requests
import datetime
from webspider.spider.jobspider.items import JobItem,CompanyItem
from webspider.baseclass.database import Database
from webspider.baseclass.baseRedis import BaseRedis
from webspider.utils.mylogger import MyLogger
from webspider.config.websetting import auth
from webspider.utils.dict_decorator import dict_decorator






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
        sql = 'select id from jobs where link="%s"'%item['link']
        if not db.query(sql):
            company = item['company']
            sql = 'select id,name from company where name="%s"'%company['name']
            redis = BaseRedis()
            if not db.query(sql):
                db.insert_by_dic('company',company)
                self.logger.info(' '.join([company['name'],u'Insert Company into Mysql Success!']))
                data = cPickle.dumps(company)
                redis.set('new_company',[data])
                self.logger.info(' '.join([company['name'], u'Insert Company into Redis Success!']))

            sql = 'select id from company where name="%s"'%company['name']
            company = db.query(sql)[0]
            try:
                item['company_id'] = company['id']
                item.pop('company')
                db.insert_by_dic('jobs',item)
                self.logger.info(' '.join([item['title'], u'Insert Job into Mysql Success from %s!'%item['website_id']]))
                day = item['pub_time'].split(' ')[0] if ':' in item['pub_time'] else item['pub_time']
                if cmp(day,self.today) == 0:
                    # serizilier,in order to get original structure from redis.
                    data = cPickle.dumps(item)
                    redis.set('latest_jobs', [data])
                    self.logger.info(' '.join([item['title'], u'Insert Job into Redis Success!']))
            except Exception,e:
                print item
                self.logger.error(u'%s::名称:%s没有正确添加。请检查.%s\n' % (self.today,item['title'],str(e)))


        return item



class LoadOnlinePipeline(object):

    def __init__(self):
        self.day = datetime.date.today().strftime("%Y-%m-%d")
        #self.file = codecs.open('store_%s.html'%self.day,'w',encoding='utf8')
        
    @dict_decorator
    def process_item(self, item, spider):
        #line = json.dumps(result,ensure_ascii=False) + "\n"
        #self.file.write(line)
        r = requests.post('http://dailyblog.applinzi.com/api/onlines/',data=item, auth=auth)
        return item

    def close_spider(self,spider):
        #when the spider is closed ,the method will be called
        #self.file.close()
        pass



class RedisLoadPipeLine(object):
    def __init__(self):
        self.day = datetime.date.today().strftime("%Y-%m-%d")
        # self.file = codecs.open('store_%s.html'%self.day,'w',encoding='utf8')

    def process_item(self, item, spider):
        """
        the redis store the jobs pubed in the cur day.
        :param item:
        :param spider:
        :return:
        """
        #print item
        redis = BaseRedis()
        redis.rs.delete('latest_jobs')
        if item['pub_time'] == self.day:
            #serizilier,in order to get original structure from redis.
            item = cPickle.dumps(item)
            redis.set('latest_jobs',[item,])

        return item


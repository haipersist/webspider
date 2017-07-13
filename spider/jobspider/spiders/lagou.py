#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import json
from cStringIO import StringIO
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
import scrapy
from webspider.baseclass.base_spider import Base_Spider
from webspider.spider.jobspider.items import JobItem,CompanyItem
from webspider.config.websetting import LgCfg




class LG_Spider(CrawlSpider):
    name = 'lagou'

    def start_requests(self):
        """
        the method aims at getting the page number.

        :return:
        """
        self.spider = Base_Spider(LgCfg)
        self.first_url = 'http://www.lagou.com/jobs/positionAjax.json?px=new&gx=%E5%85%A8%E8%81%8C&city=%E5%8C%97%E4%BA%AC&first=true&kd=python'
        response = self.spider.get_content(self.first_url,url_type='json',method='POST')
        print response
        content = response['content']["positionResult"]
        totalCount,pagesize = content["totalCount"],content["resultSize"]
        pages = totalCount/pagesize if totalCount%pagesize == 0 else totalCount/pagesize + 1
        #scrapy cookies must be dict.必须是字典形式.这和requests模块有区别。
        cookies = LgCfg.cookies()
        self.spider.headers.update({'Cookie':cookies})
        for page in range(1,pages+1):
            url = self.first_url + '&pn=%d'%page
            #print url
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 cookies=cookies,
                                 headers=self.spider.headers)

    def parse(self, response):
        """
        crawl related urls.the related url means
        the title must contains keyword python or web.
        otherwise,need to exclude these urls.

        :param response:
        :return:
        """
        content = json.load(StringIO(response.body))
        if not content:
            return
        sel = Selector(response)
        joburl = 'https://www.lagou.com/jobs/'
        for job in content['content']["positionResult"]['result']:
            positionId = job["positionId"]
            if isinstance(positionId,int):
                positionId = str(positionId)
            url = joburl + '%s.html'%positionId
            request = scrapy.Request(url=url,callback=self.parse_items,headers=self.spider.headers)
            company_item,job_item = CompanyItem(),JobItem()
            job_item['pub_time'] = job["createTime"]
            job_item['salary'] = job['salary']
            job_item['title'] = job["positionName"]
            job_item['link'] = url
            job_item['website_id'] = 1
            #job_item['welfare'] = list(job["companyLabelList"])
            company_item['name'] = job['companyFullName']
            #company_item['homepage'] =  'http://www.lagou.com/gongsi/'+str(job['companyId'])+'.html'
            request.meta['company_item'] = company_item
            request.meta['job_item'] = job_item
            yield request

    def parse_items(self,response):
        """
        This method, as well as any other Request callback,
        must return an iterable of Request and/or dicts or Item objects.
        :param response:
        :return:item
        """
        sel = Selector(response)
        #print response.url
        job_item, company_item = response.meta['job_item'], response.meta['company_item']
        company_item['introduction'] = ' '.join(sel.xpath('//ul[@class="c_feature"]/li/text()').extract())
        company_item['address'] = ''.join(sel.xpath('//div[@class="work_addr"]/a/text()').extract()[0:-1])
        company_item['homepage'] = sel.xpath('//ul[@class="c_feature"]/li[last()]/a/text()').extract_first()
        job_item['welfare'] = sel.xpath('//dd[@class="job-advantage"]/p/text()').extract_first()
        job_item['requirement'] = ' '.join(sel.xpath('//dd[@class="job_bt"]/div/p/text()').extract())
        job_item['company'] = company_item
        yield job_item






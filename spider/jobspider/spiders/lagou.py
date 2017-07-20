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
from utils.cookie2scrapy import cookie2scrapy



class LG_Spider(CrawlSpider):
    name = 'lagou'

    def start_requests(self):
        """
        the method aims at getting the page number.

        :return:
        """
        self.spider = Base_Spider(LgCfg)
        self.first_url = 'https://www.lagou.com/jobs/list_Python?px=new&gx=%E5%85%A8%E8%81%8C&city=%E5%8C%97%E4%BA%AC#order'
        """
        r = self.spider.get_content(self.first_url)
        cookies = dict(r.cookies) if not isinstance(r.cookies,dict) else r.cookies
        cookies = cookie2scrapy(cookies)
        """
        #scrapy cookies must be dict.必须是字典形式.这和requests模块有区别。
        cookies = LgCfg.cookies()
        for page in range(1,5):
            """
            #print url
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 cookies=cookies,

                                 headers=self.spider.headers)
            #the below is one method for getting data,which use post method
        """
            first = 'true' if page==1 else 'false'
            url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&gx=%E5%85%A8%E8%81%8C&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
            yield scrapy.http.FormRequest(
                url=url,
                headers=self.spider.headers,
                cookies=cookies,
                method='POST',
                formdata={
                    'kd':'Python',
                    'pn':str(page),
                    'first':first
                },
                callback=self.parse
            )


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
            request = scrapy.Request(url=url,
                                     cookies=LgCfg.cookies(),
                                     headers=LgCfg.job_header(),
                                     callback=self.parse_items
                                     )
            company_item,job_item = CompanyItem(),JobItem()
            job_item['pub_time'] = job["createTime"]
            job_item['salary'] = job['salary']
            job_item['title'] = job["positionName"]
            job_item['link'] = url
            job_item['website_id'] = 1
            job_item['welfare'] = ' '.join(job['companyLabelList'])
            #job_item['welfare'] = list(job["companyLabelList"])
            company_item['name'] = job['companyFullName']
            try:
                company_item['address'] = ' '.join(job['businessZones'])
            except TypeError:
                company_item['address'] = job['businessZones']
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
        job_item, company_item = response.meta['job_item'], response.meta['company_item']
        company_item['introduction'] = ' '.join(sel.xpath('//ul[@class="c_feature"]/li/text()').extract())
        #company_item['address'] = ''.join(sel.xpath('//div[@class="work_addr"]/a/text()').extract()[0:-1])
        company_item['homepage'] = sel.xpath('//ul[@class="c_feature"]/li[last()]/a/text()').extract_first()
        #job_item['welfare'] = sel.xpath('//dd[@class="job-advantage"]/p/text()').extract_first()
        job_item['requirement'] = ' '.join(sel.xpath('//dd[@class="job_bt"]/div/p/text()').extract())
        job_item['company'] = company_item
        #print job_item
        yield job_item






#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
import scrapy
from webspider.baseclass.base_spider import Base_Spider
from webspider.spider.jobspider.items import JobItem,CompanyItem
from webspider.config.websetting import LpCfg
from datetime import date,timedelta

class Job51_Spider(CrawlSpider):
    name = 'liepin'

    def start_requests(self):
        """
        the method aims at getting the page number.

        :return:
        """
        self.spider = Base_Spider(LpCfg)
        self.first_url = 'https://www.liepin.com/zhaopin/' \
                         '?industries=&dqs=010&salary=15%2440' \
                         '&jobKind=2&pubTime=3&compkind=&compscale=' \
                         '&industryType=&searchType=1&clean_condition=' \
                         '&isAnalysis=&init=1&sortFlag=15&flushckid=1' \
                         '&fromSearchBtn=2&headckid=0b5a9690a5cb1d82&key=Python'
        urls = []
        s = self.spider.get_content(self.first_url)
        self.cookies = self.spider.session.cookies.get_dict()
        del s
        self.spider.headers.update({'Cookie': self.cookies})
        for page in range(1,5):
            url = self.first_url + '&curPage=%d'%page
            urls.append(url)
        for url in urls:
            print url
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 headers=self.spider.headers,
                                 cookies=self.cookies
                                 )

    def parse(self, response):
        """
        crawl related urls.the related url means
        the title must contains keyword python or web.
        otherwise,need to exclude these urls.

        :param response:
        :return:
        """
        content = response.body
        if not content:
            return
        sel = Selector(response)
        #print sel.xpath('//table[@class="board-list tiz"]/tr').extract()
        for job in sel.xpath('//ul[@class="sojob-list"]/li'):
            #print 'd',job
            info = job.xpath('div[@class="sojob-item-main clearfix"]/div[@class="job-info"]')
            com_info = job.xpath('div[@class="sojob-item-main clearfix"]/div[@class="company-info nohover"]')
            title = info.xpath('h3/@title').extract_first().lower()
            if title.find('python') != -1:
               url = info.xpath('h3/a/@href').extract_first()
               print url
               request = scrapy.Request(url=url,
                                        callback=self.parse_items,
                                        headers=self.spider.headers,
                                        cookies=self.cookies)
               company_item, job_item = CompanyItem(), JobItem()
               company_item['name'] = com_info.xpath('p[@class="company-name"]/a/text()').extract_first()
               company_item['introduction'] = com_info.xpath('p[@class="company-name"]/a/@href').extract_first()
               job_item['pub_time'] = info.xpath('p[@class="time-info clearfix"]/time/text()').extract_first()
               year = str(date.today().year)
               if str(year) not in job_item['pub_time']:
                   if job_item['pub_time'] == u'昨天':
                       job_item['pub_time'] = (date.today()-timedelta(days=1)).strftime("%Y-%m-%d")
                   elif job_item['pub_time'] == u'前天':
                       job_item['pub_time'] = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
                   else:
                       job_item['pub_time'] = date.today().strftime("%Y-%m-%d")
               job_item['title'] = title
               job_item['welfare'] = ' '.join(com_info.xpath('p[@class="temptation clearfix"]/span/text()').extract())
               job_item['salary'] = info.xpath('p[@class="condition clearfix"]/span[@class="text-warning"]/text()').extract_first()
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
        item = response.meta['job_item']
        company_item = response.meta['company_item']
        company_item['address'] = ''
        item['link'] = response.url
        item['requirement'] = ' '.join(sel.xpath('//div[@class="content content-word"]/text()').extract())
        item['website_id'] = 7
        item['company'] = company_item
        print item
        yield item





if __name__ == "__main__":
    import requests
    spider = Base_Spider(LpCfg)
    first_url = 'https://www.liepin.com/zhaopin/?pubTime=7&ckid=4c6557f0055fbec6&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&dqs=010&industryType=&jobKind=2&sortFlag=15&industries=&salary=&compscale=&clean_condition=&key=Python&headckid=0b5a9690a5cb1d82&curPage=1'
    s = spider.get_content(first_url)
    print spider.session.cookies.get_dict()
    print s.find('div', attrs={'class':"sojob-result "})








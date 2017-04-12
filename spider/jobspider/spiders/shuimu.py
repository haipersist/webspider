#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
import scrapy
from webspider.baseclass.base_spider import Base_Spider
from webspider.spider.jobspider.items import JobItem,CompanyItem
from webspider.config.websetting import LpCfg,SmCfg
from datetime import date

class Job51_Spider(CrawlSpider):
    name = 'shuimu'

    def start_requests(self):
        """
        the method aims at getting the page number.

        :return:
        """
        self.spider = Base_Spider(SmCfg)
        self.first_url = 'http://www.newsmth.net/nForum/s/article?ajax&t1=python&au=&b=Career_Upgrade'
        urls = []
        s = self.spider.get_content(self.first_url)
        self.cookies = self.spider.session.cookies.get_dict()
        del s
        self.spider.headers.update({'Cookie': self.cookies})
        for page in range(1,2):
            url = self.first_url + '&p=%d'%page
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
        for job in sel.xpath('//table[@class="board-list tiz"]/tr'):
            #print 'd',job
            title = job.xpath('td[@class="title_9"]/a/text()').extract_first().lower()
            if title.find('python') != -1:
               url = 'http://www.newsmth.net' + job.xpath('td[@class="title_9"]/a/@href').extract_first()
               print url
               request = scrapy.Request(url=url,
                                        callback=self.parse_items,
                                        headers=self.spider.headers,
                                        cookies=self.cookies)
               company_item, job_item = CompanyItem(), JobItem()
               company_item['name'] = u'shuimu'
               #company_item['address'] = job.xpath('span[@class="t2"]/a/@title').extract_first()
               job_item['pub_time'] = job.xpath('td[@class="title_10"]/text()').extract_first()
               year = str(date.today().year)
               if str(year) not in job_item['pub_time']:
                   job_item['pub_time'] = year + '-' + job_item['pub_time']
                   job_item['title'] = title
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
        company_item['introduction'] = ''
        company_item['address'] = ''
        item['salary'] = ''
        item['link'] = response.url
        item['welfare'] = sel.xpath('//td[@class="a-content"]/p').extract()
        item['welfare'] = ' '.join(item['welfare'])
        item['requirement'] = sel.xpath('//td[@class="a-content"]/p').extract()
        item['requirement'] = ' '.join(item['requirement'])
        item['website_id'] = 5
        item['company'] = company_item
        print item['welfare']
        yield item





if __name__ == "__main__":
    import requests
    spider = Base_Spider(LpCfg)
    first_url = 'https://www.liepin.com/zhaopin/?pubTime=7&ckid=4c6557f0055fbec6&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&dqs=010&industryType=&jobKind=2&sortFlag=15&industries=&salary=&compscale=&clean_condition=&key=Python&headckid=0b5a9690a5cb1d82&curPage=1'
    s = spider.get_content(first_url)
    print spider.session.cookies.get_dict()
    print s.find('div', attrs={'class':"sojob-result "})








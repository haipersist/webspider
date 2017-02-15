#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
import scrapy
from webspider.baseclass.base_spider import Base_Spider
from webspider.jobspider.jobspider.items import JobItem,CompanyItem
from webspider.config.websetting import ZLCfg


class ZL_Spider(CrawlSpider):
    name = 'zhilian'

    def start_requests(self):
        """
        the method aims at getting the page number.

        :return:
        """
        self.spider = Base_Spider(ZLCfg)
        self.first_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%e5%8c%97%e4%ba%ac&kw=python&sb=1&sm=0&et=2&fl=530&isadv=0&isfilter=1&pd=3&sg=2927b4176c7d405b8628e59a64d92f5f'
        for page in range(1,4):
            url = self.first_url + '&p=%d'%page
            yield scrapy.Request(url=url,callback=self.parse,headers=self.spider.headers)

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
        for job in sel.xpath('//table[@class="newlist"]').extract()[1:]:
            title = job.xpath('/tr/td[@class="zwmc"]/div/a/text()').extract_first().lower()
            if title.find('python') != -1:
               url = job.xpath('/tr/td[@class="zwmc"]/div/a/@href').extract_first()
               request = scrapy.Request(url=url,callback=self.parse_items,headers=self.spider.headers)
               item = CompanyItem()
               item['name'] = job.xpath('/tr/td[@class="zwmc"]/a/text()').extract_first()
               item['homepage'] = job.xpath('/tr/td[@class="zwmc"]/a/@href').extract_first()
               request.meta['company_item'] = item
               yield request

    def parse_items(self,response):
        """
        This method, as well as any other Request callback,
        must return an iterable of Request and/or dicts or Item objects.
        :param response:
        :return:item
        """
        sel = Selector(response)
        item = JobItem()
        company_item = response.meta['company_item']
        company_item['introduction'] = sel.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/p/text()').extract()[1]
        company_item['address'] = sel.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/h2/text()').extract_first()
        item['salary'] = sel.xpath('//div@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li/strong/text()').extract_first()
        item['title'] = sel.xpath('//div@class="inner-left fl"]/h1/text()').extract_first()
        item['link'] = response.url
        item['welfare'] = ''
        item['requirement'] = sel.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/p/text()').extract_first()
        item['website_id'] = 3
        item['pub_time'] = sel.xpath('//div@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li/strong/text()').extract()[2]
        item['company'] = company_item
        yield item









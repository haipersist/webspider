#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
import scrapy
from datetime import date
from webspider.baseclass.base_spider import Base_Spider
from webspider.spider.jobspider.items import JobItem,CompanyItem
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
        #self.cookies = ZLCfg.cookies()
        #self.spider.headers.update({'Cookie':self.cookies})
        for page in range(1,5):
            self.url = self.first_url + '&p=%d'%page
            yield scrapy.Request(url=self.url,callback=self.parse,headers=self.spider.headers)

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
        #zhilian host is different between page list and job detail page,so this need to be changed
        self.spider.headers['Host'] = ZLCfg().jobhost
        for job in sel.xpath('//div[@class="newlist_list_content"]/table[@class="newlist"]')[1:]:
            title = job.xpath('tr/td[@class="zwmc"]/div/a/b/text()').extract_first()
            if title is not None:
               url = job.xpath('tr/td[@class="zwmc"]/div/a/@href').extract_first()
               self.spider.headers.update({'Referer':self.url})
               request = scrapy.Request(url=url,callback=self.parse_items,headers=self.spider.headers)
               item = CompanyItem()
               item['name'] = job.xpath('tr/td[@class="gsmc"]/a/text()').extract_first()
               #item['homepage'] = job.xpath('tr/td[@class="gsmc"]/a/@href').extract_first()
               request.meta['company_item'] = item
               yield request
            else:
                break

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
        company_item['homepage'] = sel.xpath('//div[@class="inner-left fl"]/h2/a/@href').extract_first()
        company_item['introduction'] = ''.join(sel.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"][last()]/p/text()').extract())
        company_item['address'] = sel.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/h2/text()').extract_first()
        item['salary'] = sel.xpath('//div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li/strong/text()').extract_first()
        item['title'] = sel.xpath('//div[@class="inner-left fl"]/h1/text()').extract_first()
        item['link'] = response.url
        item['welfare'] = ' '.join(sel.xpath('//div[class="welfare-tab-box"]/span/text()').extract())
        item['requirement'] = ' '.join(sel.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"][1]/p/text()').extract())
        item['website_id'] = 3
	pub_time = sel.xpath('//span[@id="span4freshdate"]/text()').extract_first()
        item['pub_time'] = pub_time if '2017' in pub_time else date.today().strftime("%Y-%m-%d")
	print item['pub_time'],type(item['pub_time'])
        item['company'] = company_item
        yield item









#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
import scrapy
from webspider.baseclass.base_spider import Base_Spider
from webspider.spider.jobspider.items import JobItem,CompanyItem
from webspider.config.websetting import Job51Cfg
from datetime import date

class Job51_Spider(CrawlSpider):
    name = '51job'

    def start_requests(self):
        """
        the method aims at getting the page number.

        :return:
        """
        self.spider = Base_Spider(Job51Cfg)
        self.first_url = 'http://search.51job.com/list/010000,000000,0000,00,2,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        response = self.spider.get_content(self.first_url)
        pages = response.find('span',attrs={'class':'td'}).string
        p = re.compile(r'\d{1,}')
        urls = []
        pages = int(str(p.search(pages).group()))
        self.cookies = Job51Cfg.cookies()
        self.spider.headers.update({'Cookie':self.cookies})
        for page in range(1,5):
            url = self.first_url + '&curr_page=%d'%page
            urls.append(url)
        for url in urls:
            print url
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 cookies= self.cookies,
                                 headers=self.spider.headers
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
        for job in sel.xpath('//div[@class="dw_table"]/div[@class="el"]'):
            title = job.xpath('p/span/a/@title').extract_first().lower()
            if title.find('python') != -1:
               url = job.xpath('p/span/a/@href').extract_first()
               request = scrapy.Request(url=url,callback=self.parse_items,cookies=self.cookies,headers=self.spider.headers)
               company_item, job_item = CompanyItem(), JobItem()
               company_item['name'] = job.xpath('span[@class="t2"]/a/@title').extract_first()
               #company_item['address'] = job.xpath('span[@class="t2"]/a/@title').extract_first()
               job_item['pub_time'] = job.xpath('span[@class="t5"]/text()').extract_first()
               year = str(date.today().year)
               job_item['pub_time'] = year + '-' + job_item['pub_time']
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
        company_item['introduction'] = sel.xpath('//div[@class="tmsg inbox"]/text()').extract_first()
        company_item['address'] = sel.xpath('//p[@class="fp"]/text()').extract_first()
        if not company_item['address']:
            company_item['address'] = sel.xpath('//p[@class="fp"]').extract_first()
        item['salary'] = sel.xpath('//div[@class="cn"]/strong/text()').extract_first()
        item['title'] = sel.xpath('//div[@class="cn"]/h1/@title').extract_first()
        item['link'] = response.url
        item['welfare'] = ' '.join(sel.xpath('//p[@class="t2"]/span/text()').extract())
        item['requirement'] = ''.join(sel.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract())
        if item['requirement'] is None:
            item['requirement'] = ''.join(sel.xpath('//div[@class="bmsg job_msg inbox"]/p/text()').extract())
        #print item['requirement']
        item['website_id'] = 4
        item['company'] = company_item
        yield item
















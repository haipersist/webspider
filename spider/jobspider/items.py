# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    """
    the item is used to store company information
    when scan link list,need to crawl the company name.field
    when scawl the detail job info,need to get company address
    and introduction.
    """
    name = scrapy.Field()
    address = scrapy.Field()
    introduction = scrapy.Field()
    homepage = scrapy.Field()




class JobItem(scrapy.Item):
    """
    the item is used to store job detail information
    about website field and company field is gotten from
    mysql database.
    """
    title = scrapy.Field()
    welfare = scrapy.Field()
    requirement = scrapy.Field()
    salary = scrapy.Field()
    link = scrapy.Field()
    pub_time = scrapy.Field()
    company = scrapy.Field()
    website_id = scrapy.Field()





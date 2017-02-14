#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
from baseclass.base_spider import Base_Spider
import requests



class BYR_Spider(Base_Spider):

    def __init__(self,website,*args):
        super(BYR_Spider,self).__init__(website,args)

    
    def byr_login(self):
        posturl = 'https://bbs.byr.cn/user/ajax_login.json'
        postdata = {'id':'liangting','passwd':'001108'}
        #print self.login(posturl,postdata)
        self.session = requests.Session()
        s = self.session.post(posturl,postdata,headers=self.headers)
        print self.session.get('https://bbs.byr.cn/#!s/article?t1=python&au=&b=JobInfo').content
        #print self.parse('https://bbs.byr.cn/#!s/article?t1=python&au=&b=JobInfo')


    def parse(self,url):
        try:
            soup = self.get_content(url)
        except urllib2.URLError:
            soup = self.get_content(url)
        table = soup.find('table')
        title = {'title_9':'title','title_10':'date'}
        data = []
        for tr in table.find_all('tr')[1:]:
            item = {}
            for td in tr.find_all('td')[0:-2]:
                if td['class'][0] in title.keys():
                    if td['class'][0] == 'title_9':
                        item['link'] = 'http://bbs.byr.cn'+td.a['href']
                    item[title[td['class'][0]]] = td.get_text()
                item['website'] = 'byr'
                data.append(item)
        return [item for item in data if item]

    def pages_parse(self,keyword):
        for page in xrange(1,2):
            url = 'https://bbs.byr.cn/s/article?t1=%s&au=&b=JobInfo&_uid=liangting&p=%d'%(keyword,page)
            data = self.parse(url)
            yield data






if __name__ == "__main__":
    byr = BYR_Spider('byr','X-Requested-With','Host','Referer','Cookie')
    print byr.parse('https://bbs.byr.cn/s/article?t1=python&au=&b=JobInfo&_uid=liangting')













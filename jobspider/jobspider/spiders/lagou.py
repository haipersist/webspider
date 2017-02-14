#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from hbnnwebsite.datasource.jobspider.baseclass.base_spider import Base_Spider




class LG_Spider(Base_Spider):

    def __init__(self,sitename,*args):
        #do not add host
        super(LG_Spider,self).__init__(sitename,args)
	

    def parse(self,url):
        response = self.get_content(url,url_type='json')
        content = response['content']["positionResult"]
        if hasattr(self,'total_pages'):
            self.total_pages = content["totalCount"]
        data_list = content['result']
        for data in data_list:
            item = {}
            item['website'] = 'lagou'
            item['link'] = 'http://www.lagou.com/jobs/'+str(data['positionId'])+'.html'
            item['homepage'] =  'http://www.lagou.com/gongsi/'+str(data['companyId'])+'.html'
            item['title'] = data['positionName']
            item['company'] = data['companyFullName']
            #item['salary'] = data['salary']
            item['date'] = data['createTime']
            yield item



		

    def pages_parse(self,keyword):
        for page in xrange(1,4):
            if not isinstance(keyword,unicode):
                keyword = keyword.encode('utf8')
            url = 'http://www.lagou.com/jobs/positionAjax.json?px=new&gx=%E5%85%A8%E8%81%8C&city=%E5%8C%97%E4%BA%AC&first=true&'+'kd=%s&pn=%d'%(keyword,page)
            print url
            data = self.parse(url)
            yield data



if __name__ == "__main__":
    lg = LG_Spider('lagou',"Host","Cookie")
    for data in lg.pages_parse('python'):
        for item in data:
            print item



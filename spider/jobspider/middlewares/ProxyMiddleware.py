__author__ = 'wanghb311'
#-*- coding:utf-8 -*-

from webspider.utils.Ipproxy import GetValidIP




class ProxyMiddleware(object):

    def process_reuest(self,request,spider):
        proxy = GetValidIP()
        if proxy:
            request.meta['proxy'] = proxy['http']


if __name__ == "__main__":
    proxy = GetValidIP()
    print proxy
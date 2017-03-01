import os
from webspider.config import init_env
from webspider.spider.runspider import RunSpider



init_env()

def start():
    spider = RunSpider()
    #spider.runOneSpider('zhilian')
    print 's'

start()





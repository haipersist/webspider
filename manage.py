import os
from webspider.config import init_env
from webspider.spider.runspider import RunSpider
from flask.ext.script import Manager
from flask import Flask
from webspider.da.senddata.send_daily_data import SendData

manager = Manager(Flask(__name__))


@manager.command
def initenv():
    init_env()



@manager.command
def runspiders():
    spider = RunSpider()
    spider.runMulSpider('zhilian','lagou','51job')



@manager.option('-n','--name',dest='name',default=None)
def runsinglespider(name):
    if name is None:
        print 'input spider name'
    spider = RunSpider()
    spider.runOneSpider(name)


@manager.option('-c','--category',dest='name',default='all')
def senddata(name):
    sent = SendData()
    if name == 'all':
        sent.exec_all()
    elif name == 'dailyjob':
        sent.send_daily_job()
    elif name == 'company':
        sent.send_daily_company()



if __name__ == "__main__":
    manager.run()




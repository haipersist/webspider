#-*- coding:utf-8 -*-

"""
the python file is used to start spider.In order to execute it by
using command.I use Flask-Scripts,when I learned Flask and wrote my blog
I found it is very convenient for this usage.
If you are not familiar with it.you can read the official document
about it.It's very easy to use.

   Copyright:Haibo wang. 2017

"""



import os
from webspider.config import init_env
from webspider.spider.runspider import RunSpider
from flask.ext.script import Manager
from flask import Flask
from webspider.da.senddata.send_daily_data import SendData
from webspider.da.GetNewCompany import load_online_company
from webspider.da.GetDailyJobs import load_online_job

manager = Manager(Flask(__name__))


@manager.command
def initenv():
    init_env()



@manager.command
def runspiders():
    spider = RunSpider()
    spider.runMulSpider('zhilian','lagou','51job','shuimu','liepin')

@manager.command
def load_online_data():
    load_online_company()
    load_online_job()

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




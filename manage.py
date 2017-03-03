import os
from webspider.config import init_env
from webspider.spider.runspider import RunSpider
from flask.ext.script import Manager
from flask import Flask


manager = Manager(Flask(__name__))


@manager.command
def createEnv():
    init_env()

@manager.command
def runspiders():
    spider = RunSpider()
    websites = ['zhilian','lagou','51job']
    spider.runMulSpider(websites)


@manager.option('-n','--name',dest='name',default=None)
def runsinglespider(name):
    if name is None:
        print 'print spider name'
    spider = RunSpider()
    spider.runOneSpider(name)



if __name__ == "__main__":
    manager.run()




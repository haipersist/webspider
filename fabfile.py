#-*-coding:utf-8 -*-

import os
from fabric.api import local,lcd



def push(msg):
    with lcd(os.path.join(os.path.abspath('.'))):
        local("git commit -m %s"% msg)
        local(("git push origin master"))

def startredis():
    local('nohup redis-server &')

def crawl():
    with lcd(os.path.abspath('.')):
        #local('python utils/IPProxyPool/IPProxy.py')
        local('bash run.sh')


def addproxy():
    targetpath = os.path.join(os.path.join(os.path.abspath('.'),'utils'),'IPProxyPool')
    with lcd(targetpath):
        local('nohup python IPProxy.py &')


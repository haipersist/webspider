#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import redis
import datetime
from webspider.utils.get_project_setting import get_project_setting



class BaseRedis():


    def __init__(self):
        self._connect()


    def _connect(self):
        self.setting = get_project_setting()
        config = self.setting['DATABASES']['redis']
        self.host, self.port = config['HOST'],config['PORT']

        #Implemention of Redis Protocol,this abstract class
        #provides a pythoninterface to all Redis cmds.
        self.rs = redis.StrictRedis(self.host,
                                     port=self.port,
                                     #password=self.password,
                                     )

    def set(self,name,data,expire=3600):
        """
        :param name:
        :param data: data can be any structure,dict,list,tuple,set and string.
        For every single type,use corresponding store method.
        :return:
        """
        if isinstance(data,(basestring,bytes)):
            self.rs.set(name,data)
        elif isinstance(data,list or tuple):
            for item in data:
                #add item from right side.
                self.rs.rpush(name,item)
        elif isinstance(data,set):
            for item in data:
                self.rs.sadd(name,item)
        elif isinstance(data,dict):
            self.rs.hmset(name,data)
        if not isinstance(expire,int):
            expire = 3600
        self.rs.expire(name, expire)


    def get(self,name,type='string'):
        if type == 'string':
            result = self.rs.get(name)
        elif type == 'list' or type == 'tuple':
            result = self.rs.lrange(name,0,-1)
        elif type == 'dict':
            result = self.rs.hgetall(name)
        elif type == 'set':
            result = self.rs.smembers(name)

        return result



def test():
    client=BaseRedis()
    #client.rs.delete('qw')
    data = {'s':4,'d':{'a':5}}
    import cPickle
    data = cPickle.dumps(data)
    client.set('qw',[data,])
    #client.set('oww',[12,{'s':3}])
    for item in client.get('qw',type='list'):
        print cPickle.loads(item)
    print client.rs.llen('qw')
    client.rs.delete('lina')
    print  client.get('ow')







if __name__=="__main__":
    test()



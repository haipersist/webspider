#-*-coding:utf-8 -*-
__author__ = 'wanghb311'

import copy
import warnings
from collections import MutableMapping
from importlib import import_module
from pprint import pformat  #pprint模块用来打印稍微复杂的变量，输出便于阅读。
from ..config import DATABASES,SPIDERPATH,EMAIL



class Settings(MutableMapping):

    def __init__(self):
        self.attributes = {}
        self.freeze = False

    def __contains__(self, name):
        return name in self.attributes

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    def __getitem__(self, name):
        return self.attributes[name].value

    def get(self,name,default=None):
        return self[name] if self[name] is not None else default

    def __setitem__(self, key, value):
        self.set(key,value)

    def set(self,key,value):
        self.attributes[key] = value

    def delete(self,name):
        self.assert_mutablity()
        del self.attributes[name]

    def assert_mutablity(self):
        if self.freeze:
            raise TypeError(u"该类是不可变的，不允许删除")

    def fronzen(self):
        self.freeze = True

    def copy(self):
        return copy.deepcopy(self)

    def fronzencopy(self):
        copy = self.copy()
        copy.fronzen()
        return copy




def get_project_setting():
    setting = Settings()
    setting.set('DATABASES',DATABASES)
    setting.set('SPIDERPATH',SPIDERPATH)
    setting.set('EMAIL',EMAIL)
    return setting


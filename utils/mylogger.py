#-*- coding:utf-8 -*-

import os
import logging


class MyLogger():

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.projectpath = os.environ.get('SPIDERPATH')
        print self.projectpath
        self._set_handlers()


    def _set_handlers(self):
        self.logger.addHandler(self.sta_handler)
        self.logger.addHandler(self.file_handler)

    @property
    def sta_handler(self):
        formater = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s in %(filename)s %(levelno)s'
        )
        com_handler = logging.StreamHandler()
        com_handler.setLevel(logging.ERROR)
        com_handler.setFormatter(formater)
        return com_handler

    @property
    def file_handler(self):
        self.filelog = os.path.join(self.projectpath,'logs')
        formater = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s in %(filename)s %(levelno)s'
        )
        com_handler = logging.FileHandler(os.path.join(self.filelog,'spider.log'))
        com_handler.setLevel(logging.DEBUG)
        com_handler.setFormatter(formater)
        return com_handler


if __name__ == "__main__":
    l = MyLogger('haibo').logger
    l.error('test error')
    l.warn('test warn')


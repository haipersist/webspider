#-*- coding:utf-8 -*-

import os
from datetime import date
import logging


class MyLogger():

    def __init__(self, name='webspider'):
        self.logger = logging.getLogger(name)
        self.projectpath = os.environ.get('SPIDERPATH')
        self.day = date.today().strftime("%Y-%m-%d")
        self._set_handlers()


    def _set_handlers(self):
        self.logger.addHandler(self.sta_handler)
        self.logger.addHandler(self.error_file_handler)
        self.logger.addHandler(self.info_file_handler)

    @property
    def sta_handler(self):
        formater = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s in %(filename)s %(levelno)s'
        )
        com_handler = logging.StreamHandler()
        com_handler.setLevel(logging.DEBUG)
        com_handler.setFormatter(formater)
        return com_handler

    @property
    def error_file_handler(self):
        self.filelog = os.path.join(self.projectpath,'logs')
        formater = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s in %(filename)s %(levelno)s'
        )
        com_handler = logging.FileHandler(os.path.join(self.filelog,'spiderError.log-%s'%self.day))
        com_handler.setLevel(logging.ERROR)
        com_handler.setFormatter(formater)
        return com_handler

    @property
    def info_file_handler(self):
        self.filelog = os.path.join(self.projectpath,'logs')
        formater = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s in %(filename)s %(levelno)s'
        )
        com_handler = logging.FileHandler(os.path.join(self.filelog,'spiderInfo.log-%s'%self.day))
        com_handler.setLevel(logging.INFO)
        com_handler.setFormatter(formater)
        return com_handler


if __name__ == "__main__":
    l = MyLogger('haibo').logger
    l.error('test error')
    l.warn('test warn')


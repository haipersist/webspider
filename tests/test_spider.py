#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from webspider.baseclass.base_spider import Base_Spider
from webspider.config.websetting import ZLCfg




class TestDb(unittest.TestCase):

    def test_instance(self):
        spider = Base_Spider(ZLCfg)
        assert 'Host' in spider.headers and 'Cookie' in spider.headers





if __name__ == '__main__':
    unittest.main()

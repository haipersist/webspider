#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from webspider.baseclass.database import Database


class TestDb(unittest.TestCase):

    def test_query(self):
        db = Database()
        sql = 'select * from website'
        result = db.query(sql)
        assert isinstance(result,tuple)

    def test_insert(self):
        db = Database()
        data = {
            'title':'python',
            'welfare':'fwf',
            'requirement':'wfw',
            'link':'dwdw',
            'website_id':3,
            'pub_time':'2017-02-03',
            'salary':'dwd',
            'company_id':1,
        }
        assert db.insert_by_dic('jobs',data)



if __name__ == '__main__':
    unittest.main()

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
        data = {'website':'liepin','homepage':'https://www.liepin.com'}
        assert db.insert_by_dic('website',data)



if __name__ == '__main__':
    unittest.main()

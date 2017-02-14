#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import TestCase
import unittest
from webspider.baseclass.send_email import Mail


class TestMail(TestCase):

    def test_send_txt(self):
        S_mail = Mail('myself')
        assert S_mail.send_email(msgtxt='send_email')




if __name__ == '__main__':
    unittest.main()

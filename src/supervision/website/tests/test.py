#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://docs.python.org/2/library/unittest.html

import unittest


import emailutils
from supervision.website import config

# TODO
# monkey patching python smtp lib
# www.psychicorigami.com/2007/09/20/monkey-patching-pythons-smtp-lib-for-unit-testing/


class TestSetupConfig(unittest.TestCase):

    def setUp(self):
        # Adapt the module configuration for our tests
        config.TIMEOUT = 1000
        # etc......


class TestGenerateCheckHostShScript(TestSetupConfig):
    # sh script generation
    # check all is ok
    pass


class TestCheckHostShScript(TestSetupConfig):
    # extend setup to delete the reports folder and his content
    # sh script generation
    # launch sh script to initialize folder structure
    # check : the folder exists
    # check : sitemonitor.current.status exists and is not empty
    # check : sitemonitor.previous.status exists and is empty
    # launch sh script
    # check : sitemonitor.current.status exists and is not empty
    # check : sitemonitor.previous.status exists and is not empty
    # check : sitemonitor.previous.status = initial sitemonitor.current.status
    pass


class TestReadStatus(TestSetupConfig):
    # extend setup to delete the reports folder and his content
    # sh script generation
    # launch sh script to initialize folder structure

    # set custom sitemonitor.current.status & sitemonitor.previous.status
    # with all possible configurations : SLOW_THRESHOLD, OK_STATUSES_PER_HOST..
    # verifier read_status(status_type='current')
    # verifier read_status(status_type='previous')

    pass


class TestGenerateReports(TestSetupConfig):
    # ! test only complete report lines

    # extend setup to delete the reports folder and his content
    # sh script generation
    # launch sh script to initialize folder structure

    # set custom sitemonitor.current.status
    # generate reports
    # check reports txt/html

    # set custom sitemonitor.current.status & sitemonitor.previous.status
    # generate reports
    # check reports txt/html

    pass


class TestSendMail(TestSetupConfig):
    # extend setup to delete the reports folder and his content
    # sh script generation
    # launch sh script to initialize folder structure

    # set same custom sitemonitor.current.status & sitemonitor.previous.status
    # MAIL_SEND = False, MAIL_SEND_ONLY_ON_CHANGE=False
    # generate reports
    # no mail
    # MAIL_SEND = False, MAIL_SEND_ONLY_ON_CHANGE=True
    # generate reports
    # no mail
    # MAIL_SEND = True, MAIL_SEND_ONLY_ON_CHANGE=False
    # generate reports
    # mail
    # MAIL_SEND = True, MAIL_SEND_ONLY_ON_CHANGE=True
    # generate reports
    # no mail

    # set different sitemonitor.current.status & sitemonitor.previous.status
    # MAIL_SEND = False, MAIL_SEND_ONLY_ON_CHANGE=False
    # generate reports
    # no mail
    # MAIL_SEND = False, MAIL_SEND_ONLY_ON_CHANGE=True
    # generate reports
    # no mail
    # MAIL_SEND = True, MAIL_SEND_ONLY_ON_CHANGE=False
    # generate reports
    # mail
    # MAIL_SEND = True, MAIL_SEND_ONLY_ON_CHANGE=True
    # generate reports
    # mail

    # test from/to... on the last message

    pass


if __name__ == '__main__':
    unittest.main()

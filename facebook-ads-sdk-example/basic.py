# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

import sys, os
import time
import datetime
import logging
try:
	import ConfigParser
except:
	import configparser as ConfigParser
import simplejson as json
import requests
import unittest

from facebookads import FacebookSession
from facebookads import FacebookAdsApi
from facebookads.objects import (
	AdUser,
)


class BasicManager(object):
	''' 测试Facebook新功能
	'''
	me = AdUser(fbid='me') # user account
	
	def __init__(self, conf):
		self.app_id = conf.get('FB_Authentication', 'app_id')
		self.app_secret = conf.get('FB_Authentication', 'app_secret')
		self.access_token = conf.get('FB_Authentication', 'access_token')
		self.session = FacebookSession(self.app_id, self.app_secret, self.access_token)
		self.api = FacebookAdsApi(self.session)
		FacebookAdsApi.set_default_api(self.api)

	def run(self, now, logger):
		try:
			logger.info('Hello, BasicManager Run')
		except Exception as e:
			logger.exception(e)


class BasicManagerTest(unittest.TestCase):
	''' Basic Manager Test
	'''
	def setUp(self):
		basepath = os.path.abspath(os.getcwd())
		confpath = os.path.join(basepath, 'conf/test.conf')
		self.conf = ConfigParser.RawConfigParser()
		self.conf.read(confpath)
		
		print basepath
		logging.basicConfig(filename=os.path.join(basepath, 'logs/test.log'), level=logging.INFO,
			format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
			datefmt = '%a, %d %b %Y %H:%M:%S'
			)
		self.logger = logging.getLogger('Test')

	def tearDown(self):
		pass


if __name__ == '__main__':

	basepath = os.path.abspath(os.getcwd())
	confpath = os.path.join(basepath, 'conf/test.conf')
	conf = ConfigParser.RawConfigParser()
	conf.read(confpath)
	
	logging.basicConfig(filename=os.path.join(basepath, 'logs/test.log'), level=logging.INFO,
		format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
		datefmt = '%a, %d %b %Y %H:%M:%S'
		)
	logger = logging.getLogger('Test')

	try:
		now = time.localtime()
		BasicManager(conf).run(now, logger)	
	except Exception,e:
		logging.exception(e)


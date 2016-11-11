# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

import os
import sys
import logging
try:
	import ConfigParser
except ImportError:
	import configparser as ConfigParser
import unittest


class APIManagerTest(unittest.TestCase):
	""" Basic API Manager Test
	"""
	def setUp(self):
		basepath = os.path.abspath(os.getcwd())
		confpath = os.path.join(basepath, 'conf/test.conf')
		self.conf = ConfigParser.RawConfigParser()
		self.conf.read(confpath)
		
		logging.basicConfig(filename=os.path.join(basepath, 'logs/test.log'), level=logging.INFO,
			format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
			datefmt = '%a, %d %b %Y %H:%M:%S'
		)
		self.logger = logging.getLogger()

	def tearDown(self):
		pass


if __name__ == '__main__':
	unittest.main()

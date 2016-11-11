# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

import os
import sys
import logging
import unittest
from creative_related import CreativeManager
from test_basic import APIManagerTest


class CreativeManagerTest(APIManagerTest):
	""" Test Creative Related Work
	"""
	def setUp(self):
		super(CreativeManagerTest, self).setUp()

		self.bm = CreativeManager(self.conf)

	def test_build_image_creative(self):
		logger = self.logger

		account_id = 'YOUR_ACCOUNT_ID'
		promotion_url = 'YOUR_PROMOTION_URL'
		fb_page_id = 'YOUR_PAGE_ID'
		fb_image_id = 'YOUR_IMAGE_ID'
		title = 'test-title'
		body = 'test-body'
	
		# build facebook image creative	
		fb_creative = self.bm.build_image_creative(account_id, promotion_url, fb_image_id, title, body, fb_page_id, self.logger)
		logger.info('build fb_creative[%d]' % int(fb_creative['id']))

		# build instagram image creative
		instagram_actor_id = 'YOUR_INSTAGRAM_ID'
		fb_creative = self.bm.build_image_creative(account_id, promotion_url, fb_image_id, title, body, fb_page_id, self.logger, instagram_actor_id)
		logger.info('build instagram_creative[%d]' % int(fb_creative['id']))

	@unittest.skip('skip')
	def test_build_video_creative(self):
		logger = self.logger

		account_id = 'YOUR_ACCOUNT_ID'
		promotion_url = 'YOUR_PROMOTION_URL'
		fb_page_id = 'YOUR_PAGE_ID'
		title = 'test-title'
		body = 'test-body'
		video_id = 'YOUR_VIDEO_ID'
		video_image_url = 'VIDEO_COVER_IMG_URL'
	
		# build facebook video creative	
		self.bm.build_video_creative(account_id, promotion_url, video_id, video_image_url, title, body, fb_page_id, logger)

		# build instagram video creative
		instagram_actor_id = 'YOUR_INSTAGRAM_ID'
		self.bm.build_video_creative(account_id, promotion_url, video_id, video_image_url, title, body, fb_page_id, logger, instagram_actor_id)

	@unittest.skip('skip')
	def test_build_carousel_creative(self):
		logger = self.logger

		account_id = 'YOUR_ACCOUNT_ID'
		promotion_url = 'YOUR_PROMOTION_URL'
		fb_page_id = 'YOUR_PAGE_ID'
		fb_image_id = []
		title = 'test-title'
		sub_title = 'test-sub-title'
		body = 'test-body'
	
		# build facebook carousel creative	
		self.bm.build_carousel_creative(account_id, promotion_url, title, sub_title, body, fb_image_ids, fb_page_id, logger)

		# build instagram carousel creative
		instagram_actor_id = 'YOUR_INSTAGRAM_ID'
		self.bm.build_carousel_creative(account_id, promotion_url, title, sub_title, body, fb_image_ids, fb_page_id, logger, instagram_actor_id)


if __name__ == '__main__':
	unittest.main()

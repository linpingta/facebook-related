# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

import unittest

from basic import BasicManager, BasicManagerTest
from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	AdCreative,
)


class CreativeManager(BasicManager):

	def __init__(self, conf):
		super(CreativeManager, self).__init__(conf)

	def build_image_creative(self, account_id, promotion_url, fb_image_id, title, body, fb_page_id, logger, instagram_actor_id=0):
		''' create facebook / instagram single-image creative'''
		try:
			object_story_spec = ObjectStorySpec()

			# build Link-Ad
			call_to_action = {
				'type': 'INSTALL_MOBILE_APP',
				'value': {
					'link': promotion_url,
				}
			}
			link_data = LinkData()
			link_data[LinkData.Field.link] = promotion_url
			link_data[LinkData.Field.call_to_action] = call_to_action
			link_data[LinkData.Field.message] = body
			link_data[LinkData.Field.image_hash] = fb_image_id

			# add to object_story_spec
			object_story_spec[ObjectStorySpec.Field.link_data] = link_data
			object_story_spec[ObjectStorySpec.Field.page_id] = fb_page_id
			if instagram_actor_id:
				object_story_spec[ObjectStorySpec.Field.instagram_actor_id] = instagram_actor_id

			# creative creation
			fb_creative = AdCreative(parent_id='act_' + str(account_id))
			fb_creative.update({
				AdCreative.Field.object_story_spec : object_story_spec
			})
			fb_creative.remote_create()

			return fb_creative
		except Exception as e:
			logger.exception(e)

	def build_video_creative(self, account_id, promotion_url, video_id, video_image_url, title, body, fb_page_id, logger, instagram_actor_id=0):
		''' create facebook/instagram video creative'''
		try:
			video_data = VideoData()
			video_data[VideoData.Field.video_id] = video_id
			video_data[VideoData.Field.image_url] = video_image_url
			video_data[VideoData.Field.description] = body
			video_data[VideoData.Field.call_to_action] = {
				'type': 'INSTALL_MOBILE_APP',
				'value': {
					'link_title': title,
					'link': promotion_url,
				}
			}

			object_story_spec = ObjectStorySpec()
			object_story_spec[ObjectStorySpec.Field.page_id] = fb_page_id
			object_story_spec[ObjectStorySpec.Field.video_data] = video_data
			if instagram_actor_id:
				object_story_spec[ObjectStorySpec.Field.instagram_actor_id] = instagram_actor_id

			fb_creative = AdCreative(parent_id='act_' + str(account_id))
			fb_creative.update({
				AdCreative.Field.object_story_spec : object_story_spec
			})
			fb_creative.remote_create()

			return fb_creative
		except Exception as e:
			logger.exception(e)

	def build_carousel_creative(self, account_id, promotion_url, title, sub_title, body, fb_image_ids, fb_page_id, logger, instagram_actor_id=0):
		''' create facebook/instagram carousel creative'''
		try:
			# build Link-Ad
			call_to_action = {
				'type': 'INSTALL_MOBILE_APP',
				'value': {
					'link_title': sub_title,
					'link': promotion_url,
				}
			}
			child_attachments = []
			for i in range(len(fb_image_ids)):
				attachment_data = AttachmentData()
				attachment_data[AttachmentData.Field.call_to_action] = call_to_action
				attachment_data[AttachmentData.Field.name] = 'name %d' % i
				attachment_data[AttachmentData.Field.description] = 'description %d' % i
				attachment_data[AttachmentData.Field.image_hash] = fb_image_ids[i]
				attachment_data[AttachmentData.Field.link] = promotion_url

				child_attachments.append(attachment_data)

			link_data = LinkData()
			link_data[LinkData.Field.link] = promotion_url
			link_data[LinkData.Field.child_attachments] = child_attachments
			link_data[LinkData.Field.multi_share_optimized] = True
			link_data[LinkData.Field.call_to_action] = call_to_action
			link_data[LinkData.Field.message] = body

			object_story_spec = ObjectStorySpec()
			object_story_spec[ObjectStorySpec.Field.page_id] = fb_page_id
			object_story_spec[ObjectStorySpec.Field.link_data] = link_data

			fb_creative = AdCreative(parent_id='act_' + str(account_id))
			fb_creative.update({
				AdCreative.Field.object_story_spec : object_story_spec
			})
			fb_creative.remote_create()

			return fb_creative
		except Exception as e:
			logger.exception(e)


class CreativeManagerTest(BasicManagerTest):
	''' Test Creative Related Work
	'''
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

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

from facebookads import FacebookSession
from facebookads import FacebookAdsApi
from facebookads.objects import (
	AdUser,
	AdAccount,
	Campaign,
	AdSet,
	Ad,
	AdCreative,
	TargetingSpecsField,
	CustomAudience,
	LookalikeAudience,
)
from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData


class TestManager(object):
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

		self.instagram_actor_id = conf.getint('FB_Authentication', 'instagram_actor_id')
		self.account_id = conf.get('FB_Authentication', 'account_id')
		self.promotion_url = conf.get('FB_Authentication', 'promotion_url')
		self.promotion_id = conf.get('FB_Authentication', 'promotion_id')
		self.fb_page_id = conf.get('FB_Authentication', 'fb_page_id')
		self.fb_image_id = conf.get('FB_Authentication', 'fb_image_id')
		fb_image_ids = conf.get('FB_Authentication', 'fb_image_ids')
		self.fb_image_ids = fb_image_ids.split(',')

		self.video_id = conf.get('FB_Authentication', 'video_id')
		self.video_image_url = conf.get('FB_Authentication', 'video_image_url')

	def _build_instagram_creative(self, logger):
		''' 创建instagram广告'''
		
		# build Link-Ad
		link_data = LinkData()
		link_data[LinkData.Field.link] = self.promotion_url

		body = 'Learn more about Chinese Kongfu with Taichi panda! RPG No.1 !'

		object_story_spec = ObjectStorySpec()
		fb_creative = AdCreative(parent_id='act_' + str(self.account_id))
		call_to_action = {
			'type': 'INSTALL_MOBILE_APP',
			'value': {
				'link': self.promotion_url,
			}
		}
		link_data[LinkData.Field.call_to_action] = call_to_action
		link_data[LinkData.Field.message] = body
		#link_data[LinkData.Field.image_crops] = {
		#	'100x100':[[10, 10], [610, 610]]
		#}
		link_data[LinkData.Field.image_hash] = self.fb_image_id

		object_story_spec[ObjectStorySpec.Field.page_id] = self.fb_page_id
		object_story_spec[ObjectStorySpec.Field.link_data] = link_data
		object_story_spec[ObjectStorySpec.Field.instagram_actor_id] = self.instagram_actor_id

		fb_creative.update({
			AdCreative.Field.object_story_spec : object_story_spec
		})
		fb_creative.remote_create()

		return fb_creative

	def _build_instagram_carousel_creative(self, logger):
		''' 创建app install广告'''
		
		# build Link-Ad
		link_data = LinkData()
		link_data[LinkData.Field.link] = self.promotion_url

		title = 'mock_title'
		body = 'mock_body'

		sub_title = 'mock_sub_title'

		object_story_spec = ObjectStorySpec()
		object_story_spec[ObjectStorySpec.Field.page_id] = self.fb_page_id
		fb_creative = AdCreative(parent_id='act_' + str(self.account_id))
		call_to_action = {
			'type': 'INSTALL_MOBILE_APP',
			'value': {
				'link_title': sub_title,
				'link': self.promotion_url,
			}
		}
		
		child_attachments = []
		for i in range(3):
			attachment_data = AttachmentData()
			attachment_data[AttachmentData.Field.call_to_action] = call_to_action
			attachment_data[AttachmentData.Field.name] = 'name %d' % i
			attachment_data[AttachmentData.Field.description] = 'desc %d' % i
			attachment_data[AttachmentData.Field.image_hash] = self.fb_image_ids[i]
			attachment_data[AttachmentData.Field.link] = self.promotion_url

			child_attachments.append(attachment_data)

		link_data[LinkData.Field.child_attachments] = child_attachments
		link_data[LinkData.Field.multi_share_optimized] = True
		link_data[LinkData.Field.call_to_action] = call_to_action
		link_data[LinkData.Field.message] = body
		link_data[LinkData.Field.link] = self.promotion_url
		#link_data[LinkData.Field.image_crops] = {
		#	'100x100':[[10, 10], [610, 610]]
		#}

		object_story_spec[ObjectStorySpec.Field.link_data] = link_data
		object_story_spec[ObjectStorySpec.Field.instagram_actor_id] = 842776182467677

		fb_creative.update({
			AdCreative.Field.object_story_spec : object_story_spec
		})
		fb_creative.remote_create()

		return fb_creative

	def update_creative_text(self, fb_ad_id, fb_creative_id, logger):
		''' 更新创意文案'''
		fb_creative = AdCreative(str(fb_creative_id))
		fb_creative.remote_read(
			fields=[AdCreative.Field.id, AdCreative.Field.object_story_spec]
		)
		new_object_story_spec = ObjectStorySpec()

		old_object_story_spec = fb_creative[AdCreative.Field.object_story_spec]
		new_object_story_spec[ObjectStorySpec.Field.page_id] = old_object_story_spec['page_id']

		old_link_data = old_object_story_spec[ObjectStorySpec.Field.link_data]
		new_link_data = LinkData()
		new_link_data[LinkData.Field.link] = old_link_data['link']
		new_link_data[LinkData.Field.call_to_action] = old_link_data['call_to_action']
		new_link_data[LinkData.Field.image_hash] = old_link_data['image_hash']
		new_title = 'Great SMS Themes for Android'
		new_body = 'Themes are Free to Download!'
		new_link_data[LinkData.Field.caption] = new_title
		new_link_data[LinkData.Field.message] = new_body

		new_object_story_spec[ObjectStorySpec.Field.link_data] = new_link_data
		print type(new_object_story_spec)
		print new_object_story_spec

		#fb_creative.update({
		#	AdCreative.Field.object_story_spec : new_object_story_spec
		#})
		fb_creative[AdCreative.Field.name] = 'new test'
		fb_creative[AdCreative.Field.object_story_spec] = new_object_story_spec
		print fb_creative.remote_update()
		print 'update creative text'

		#fb_creative_id = fb_creative[AdCreative.Field.id]
		#ad = Ad(str(fb_ad_id))
		#ad.update({
		#	Ad.Field.creative:{
		#		Ad.Field.Creative.creative_id: fb_creative_id,
		#	},
		#})
		#ad.remote_update()
		#print 'update ad'

	def _build_creative(self, logger):
		''' 创建app install广告'''
		
		# build Link-Ad
		link_data = LinkData()
		link_data[LinkData.Field.link] = self.promotion_url

		title = 'mock_title'
		body = 'mock_body'

		object_story_spec = ObjectStorySpec()
		object_story_spec[ObjectStorySpec.Field.page_id] = self.fb_page_id
		fb_creative = AdCreative(parent_id='act_' + str(self.account_id))
		call_to_action = {
			'type': 'INSTALL_MOBILE_APP',
			'value': {
				'link_title': title,
				'link': self.promotion_url,
			}
		}
		link_data[LinkData.Field.call_to_action] = call_to_action
		link_data[LinkData.Field.caption] = title
		link_data[LinkData.Field.message] = body
		link_data[LinkData.Field.image_hash] = self.fb_image_id

		object_story_spec[ObjectStorySpec.Field.link_data] = link_data

		fb_creative.update({
			AdCreative.Field.object_story_spec : object_story_spec
		})
		fb_creative.remote_create()

		return fb_creative

	def _build_instagram_video_creative(self, logger):
		''' 创建app install广告'''
		
		title = 'mock_title'

		video_data = VideoData()
		video_data[VideoData.Field.description] = 'My Description'
		video_data[VideoData.Field.video_id] = self.video_id
		video_data[VideoData.Field.image_url] = self.video_image_url
		video_data[VideoData.Field.call_to_action] = {
			'type': 'INSTALL_MOBILE_APP',
			'value': {
				'link_title': title,
				'link': self.promotion_url,
			}
		}

		object_story_spec = ObjectStorySpec()
		object_story_spec[ObjectStorySpec.Field.page_id] = self.fb_page_id
		object_story_spec[ObjectStorySpec.Field.video_data] = video_data
		object_story_spec[ObjectStorySpec.Field.instagram_actor_id] = self.instagram_actor_id

		fb_creative = AdCreative(parent_id='act_' + str(self.account_id))
		fb_creative.update({
			AdCreative.Field.object_story_spec : object_story_spec
		})
		fb_creative.remote_create()

		return fb_creative

	def _build_video_creative(self, logger):
		''' 创建app install广告'''
		
		title = 'mock_title'

		video_data = VideoData()
		#video_data[VideoData.Field.description] = 'My Description'
		video_data[VideoData.Field.video_id] = self.video_id
		video_data[VideoData.Field.image_url] = self.video_image_url
		video_data[VideoData.Field.call_to_action] = {
			'type': 'INSTALL_MOBILE_APP',
			'value': {
				'link': self.promotion_url,
			}
		}

		object_story_spec = ObjectStorySpec()
		object_story_spec[ObjectStorySpec.Field.page_id] = self.fb_page_id
		object_story_spec[ObjectStorySpec.Field.video_data] = video_data

		fb_creative = AdCreative(parent_id='act_' + str(self.account_id))
		fb_creative.update({
			AdCreative.Field.object_story_spec : object_story_spec
		})
		fb_creative.remote_create()

		return fb_creative

	def _build_carousel_creative(self, logger):
		''' 创建app install广告'''
		
		# build Link-Ad
		link_data = LinkData()
		link_data[LinkData.Field.link] = self.promotion_url

		title = 'mock_title'
		body = 'mock_body'

		sub_title = 'mock_sub_title'

		object_story_spec = ObjectStorySpec()
		object_story_spec[ObjectStorySpec.Field.page_id] = self.fb_page_id
		fb_creative = AdCreative(parent_id='act_' + str(self.account_id))
		call_to_action = {
			'type': 'INSTALL_MOBILE_APP',
			'value': {
				'link_title': sub_title,
				'link': self.promotion_url,
			}
		}

		child_attachments = []
		for i in range(3):
			attachment_data = AttachmentData()
			attachment_data[AttachmentData.Field.call_to_action] = call_to_action
			attachment_data[AttachmentData.Field.name] = 'name %d' % i
			attachment_data[AttachmentData.Field.description] = 'desc %d' % i
			attachment_data[AttachmentData.Field.image_hash] = self.fb_image_ids[i]
			attachment_data[AttachmentData.Field.link] = self.promotion_url

			child_attachments.append(attachment_data)

		link_data[LinkData.Field.child_attachments] = child_attachments
		link_data[LinkData.Field.multi_share_optimized] = True
		link_data[LinkData.Field.call_to_action] = call_to_action
		link_data[LinkData.Field.message] = body
		link_data[LinkData.Field.link] = self.promotion_url

		object_story_spec[ObjectStorySpec.Field.link_data] = link_data

		fb_creative.update({
			AdCreative.Field.object_story_spec : object_story_spec
		})
		fb_creative.remote_create()

		return fb_creative

	def _build_instagram_adset(self, campaign_id, cur_time, begin_time, end_time, logger):
		''' Instagram Adset'''
		#bid_type = AdSet.BidType.absolute_ocpm
		bid_info = { 
			AdSet.Field.BidInfo.actions: 10, 
		}
		bid_amount = 400
		# Android
		#adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["mobilefeed", "instagramstream"], "user_os": ["Android_ver_2.3_and_above"], "age_min": "28", "genders": [1]}
		#adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["instagramstream"], "user_os": ["Android_ver_2.3_and_above"], "age_min": "28", "genders": [1]}

		# IOS
		#adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "30", "page_types": ["mobilefeed", "instagramstream"], "user_os": ["iOS_ver_6.0_and_above"], "age_min": "15"}
		# TEST
		adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "13", "page_types": ["mobilefeed", "instagramstream"], "user_os": ["iOS_ver_2.0_and_above"], "age_min": "13", "genders": [1], "wireless_carrier": ["wifi"]}

		promoted_object = {"object_store_url": self.promotion_url, "application_id": self.promotion_id}

		ad_set = AdSet(parent_id='act_' + str(self.account_id))
		ad_set.update({
			AdSet.Field.name: 'Domob_taichipandan_insta_test_test_3_adset',
			AdSet.Field.status: AdSet.Status.active,
			AdSet.Field.bid_amount: bid_amount,
			#AdSet.Field.bid_info: bid_info,
			AdSet.Field.billing_event : AdSet.BillingEvent.impressions,
			AdSet.Field.optimization_goal : AdSet.OptimizationGoal.app_installs,
			AdSet.Field.promoted_object: json.dumps(promoted_object),
			AdSet.Field.daily_budget: '10000',
			AdSet.Field.created_time: str(cur_time),
			AdSet.Field.start_time: str(begin_time),
			#AdSet.Field.end_time: str(end_time),
			AdSet.Field.campaign_group_id: str(campaign_id),
			AdSet.Field.targeting: json.dumps(adset_target_dict)
		})
		ad_set.remote_create()

		return ad_set

	def _build_adset(self, campaign_id, cur_time, begin_time, end_time, logger):
		''' Common Adset'''
		bid_info = { 
			AdSet.Field.BidInfo.actions: 10, 
		}
		bid_amount = 100
		# Android
		#adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["mobilefeed"], "user_os": ["Android_ver_2.3_and_above"], "age_min": "28", "genders": [1]}
		# IOS
		adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["mobilefeed"], "user_os": ["iOS_ver_6.0_and_above"], "age_min": "28", "genders": [1]}

		promoted_object = {"object_store_url": self.promotion_url, "application_id": self.promotion_id}

		ad_set = AdSet(parent_id='act_' + str(self.account_id))
		ad_set.update({
			AdSet.Field.name: 'video_test_5_adset',
			AdSet.Field.status: AdSet.Status.active,
			AdSet.Field.bid_amount: bid_amount,
			#AdSet.Field.bid_info: bid_info,
			AdSet.Field.billing_event : AdSet.BillingEvent.impressions,
			AdSet.Field.optimization_goal : AdSet.OptimizationGoal.app_installs,
			AdSet.Field.promoted_object: json.dumps(promoted_object),
			AdSet.Field.daily_budget: '100',
			AdSet.Field.created_time: str(cur_time),
			AdSet.Field.start_time: str(begin_time),
			AdSet.Field.end_time: str(end_time),
			AdSet.Field.campaign_group_id: str(campaign_id),
			AdSet.Field.targeting: json.dumps(adset_target_dict)
		})
		ad_set.remote_create()

		return ad_set

	def run(self, logger):
		''' 执行测试操作'''
		# now
		cur_time = int(time.time())
		begin_time = cur_time
		end_time = cur_time + 360000

		# create campaign
		campaign = Campaign(parent_id='act_' + str(self.account_id))
		campaign.update({
			Campaign.Field.name: 'we1_video_campaign_test',
			Campaign.Field.objective: Campaign.Objective.mobile_app_installs,
			Campaign.Field.status: Campaign.Status.paused,
			Campaign.Field.buying_type: Campaign.BuyingType.auction,
		})
		campaign.remote_create()
		campaign_id = int(campaign[Campaign.Field.id])
		logger.debug('create campaign cpid[%d]' % campaign_id)

		# create adset
		ad_set = self._build_adset(campaign_id, cur_time, begin_time, end_time, logger)
		#ad_set = self._build_instagram_adset(campaign_id, cur_time, begin_time, end_time, logger)
		adset_id = int(ad_set[AdSet.Field.id])
		logger.debug('create adset adset_id[%d]' % adset_id)

		# create creative
		#fb_creative = self._build_carousel_creative(logger)
		#fb_creative = self._build_instagram_creative(logger)
		#fb_creative = self._build_instagram_video_creative(logger)
		fb_creative = self._build_video_creative(logger)
		#fb_creative = self._build_instagram_carousel_creative(logger)
		#fb_creative = self._build_creative(logger)
		fb_creative_id = int(fb_creative[AdCreative.Field.id])
		logger.debug('create creative fb_creative_id[%d]' % fb_creative_id)

		# create ad
		ad = Ad(parent_id='act_' + str(self.account_id))
		ad.update({
			Ad.Field.name: '_'.join(['vido_test_3', str(fb_creative_id)]),
			Ad.Field.status: Ad.Status.active,
			Ad.Field.campaign_id: adset_id,
			Ad.Field.creative: {
				Ad.Field.Creative.creative_id: fb_creative_id,
			},
		})
		ad.remote_create()
		ad_id = int(ad[Ad.Field.id])
		logger.debug('create ad ad_id[%d]' % ad_id)

	def get_stats(self, logger):
		# read stats
		print 'test'
		id_str = json.loads(str([6034639791848]))
		start_time = '1440432000'
		end_time = '1440518399'
		#params = { 
		#	'adgroup_ids' : id_str,
		#	'start_time' : start_time,
		#	'end_time' : end_time
		#}
		# v2.4
		params = {
			'time_range':{'since':'2016-03-01', 'until':'2016-03-01'},
			'level':'account',
			#'fields':['spend', 'frequency', 'reach', 'clicks', 'impressions', 'actions', 'relevance_score', 'adgroup_id'],
			#'filtering':[{'field':'adgroup.id', 'operator':'IN', 'value':['6034639791848']}]
		}

		#account "= AdAccount(act_" + str(self.account_id))
		#adgroup_list = account.get_ad_group_stats(params=params)
		#for ad_group_stats in adgroup_list:
		#	adgroup_id = long(ad_group_stats['adgroup_id'])
		#	print adgroup_id

		#	for key, item in ad_group_stats.iteritems():
		#		print key, item
		#ad = Campaign(str(6032302001209))
		#insights = ad.get_insights(params=params)

		#account = AdAccount("act_" + str(833588380050856))
		account = AdAccount("act_" + str(560293150819181))
		insights = account.get_insights(params=params)
		for insight in insights:
			print insight
		print len(insights)

	def get_yesterday_stats(self, account_id, now, logger):
		account = AdAccount('act_' + str(account_id))
		before_dt = datetime.datetime.fromtimestamp(time.mktime(now)) - datetime.timedelta(days=1)
		before_t = before_dt.timetuple()
		before_day = str(time.strftime('%Y-%m-%d', before_t))
		params = {
			'time_range':{'since':before_day, 'until':before_day},
			'level':'account',
			'fields':['spend'],
		}
		insights = account.get_insights(params=params)
		spent = 0
		if insights:
			spent = insights[0]['spend']
		print spent

	def get_account_info(self, logger):
		''' get account info'''
		account = AdAccount('act_'+str(419243954950143))
		account.remote_read(fields=[AdAccount.Field.spend_cap, AdAccount.Field.amount_spent, AdAccount.Field.name])
		print account[AdAccount.Field.spend_cap]
		print account[AdAccount.Field.name]
		print account[AdAccount.Field.amount_spent]
	
	def get_account_stats(self, account_id ,start_dt, end_dt, logger):
		# read stats
		account_stats = {}
		params = {
			'time_range':{'since':start_dt, 'until':end_dt},
			'fields':['spend'],
		}

		account = AdAccount('act_' + str(account_id))
		insights = account.get_insights(params=params)
		account_stats['spend'] = float(insights[0]['spend'])
		account_stats['start_dt'] = start_dt
		account_stats['end_dt'] = end_dt
		account_stats['account_id'] = account_id
		return account_stats

	def get_campaign_stats(self, campaign_id, dt, logger):
		# read stats
		print 'campaign'
		id_str = json.loads(str([campaign_id]))
		# v2.4
		params = {
			'time_range':{'since':dt, 'until':dt},
			'level':'campaign_group',
			#'fields':['spend', 'frequency', 'reach', 'clicks', 'impressions', 'actions', 'campaign_group_id'],
			#'filtering':[{'field':'campaign_group_id', 'operator':'IN', 'value':[str(campaign_id)]}]
		}

		#account "= AdAccount(act_" + str(self.account_id))
		#adgroup_list = account.get_ad_group_stats(params=params)
		#for ad_group_stats in adgroup_list:
		#	adgroup_id = long(ad_group_stats['adgroup_id'])
		#	print adgroup_id

		#account = AdAccount("act_" + str(account_id))
		#insights = account.get_insights(params=params)
		campaign = Campaign(str(campaign_id))
		insights = campaign.get_insights(params=params)
		for insight in insights:
			print insight
			logger.info(insight)
		print len(insights)

	def create_lookalike_audience(self, logger):
		''' create lookalike audience'''
		l_audience = LookalikeAudience(parent_id = "act_" + str(876315309111496))
		l_audience.update({
			LookalikeAudience.Field.name: 'test_ct',
			LookalikeAudience.Field.LookalikeSpec.ratio : 0.01,
			LookalikeAudience.Field.LookalikeSpec.country : 'US',
			LookalikeAudience.Field.LookalikeSpec.pixel_ids : ['6034131149644'],
			LookalikeAudience.Field.LookalikeSpec.conversion_type : 'campaign_conversions',
			LookalikeAudience.Field.LookalikeSpec.type : 'similarity'
			})

		l_audience.remote_create()
		print 'Audience'
		print l_audience[LookalikeAudience.Field.id]

	def create_ad_account(self, logger):
		print 'create ad account'
		try:
			r = requests.post('https://graph.facebook.com/v2.4/694873303966595/adaccount?name=dummy&currency=USD&timezone_id=62&end_advertiser=NONE&media_agency=NONE&partner=NONE&invoice=true&access_token=CAAIeFK5hGC8BAJybd6KrswY6Nx49dGtyKL0nAnTMMKKZAtpnOySgnBQ7yicYcpXs3ubqZAvuUuGWFOWdZCZBXS2DHsIsBHuSdZBk1IeamN7Pg5PVe0KexmcnTxxGhWzRlKaCN3fYFrZAwKO7gP2YdspmpXRZBv7V5IUoyOfE3se2mxPNgeZAQNrfb3kvtwSodg9P3fZAPaDatFAZDZD')
			#r = requests.post('https://graph.facebook.com/v2.4/1717296325212302/adaccount?name=dummy&currency=USD&timezone_id=62&end_advertiser=NONE&media_agency=NONE&partner=NONE&invoice=true&access_token=CAAIeFK5hGC8BAJybd6KrswY6Nx49dGtyKL0nAnTMMKKZAtpnOySgnBQ7yicYcpXs3ubqZAvuUuGWFOWdZCZBXS2DHsIsBHuSdZBk1IeamN7Pg5PVe0KexmcnTxxGhWzRlKaCN3fYFrZAwKO7gP2YdspmpXRZBv7V5IUoyOfE3se2mxPNgeZAQNrfb3kvtwSodg9P3fZAPaDatFAZDZD')
			print r.json()
		except Exception, e:
			logger.exception(e)

	def delete_campaign(self, fb_campaign_id, logger):
		try:
			if fb_campaign_id > 0:
				campaign = Campaign(str(fb_campaign_id))
				campaign.remote_delete()
				logger.warning('fb_cpid[%d] deleted' % fb_campaign_id)
			else:
				logger.warning('fb_cpid[%d] invalid for fb delete' % fb_campaign_id)
			return 0	
		except Exception, e:
			logger.exception(e)

	def query_info(self, logger):
		account_id = 419243954950143
		account = AdAccount('act_' + str(account_id))
		campaigns = account.get_ad_campaigns(fields=[
			Campaign.Field.id,
			Campaign.Field.name,
			Campaign.Field.status,
			Campaign.Field.is_completed,
		])
		print 'test'
		#zeus_spec_cpids = [6034639791848, 6034642264048,6034642351648,6034643646248,6034644235648,6034644804448,6034645170248,6034645525848,6034645980448]
		for campaign in campaigns:
			fb_campaign_id = int(campaign[Campaign.Field.id]) 
			if fb_campaign_id not in zeus_spec_cpids:
				continue
			print fb_campaign_id, str(campaign[Campaign.Field.status])
			#logger.debug('cpid[%d]', fb_campaign_id)
			#logger.debug('status %s', str(campaign[Campaign.Field.status]))

	def query_campaign_info(self, campaign_id, logger):
		campaign = Campaign(str(campaign_id))
		campaign.remote_read(fields=[
			Campaign.Field.id,
			Campaign.Field.name,
			Campaign.Field.status,
		])
		print 'campaign info'
		print campaign[Campaign.Field.id]
		print campaign[Campaign.Field.name]
		print campaign[Campaign.Field.status]

	def pause_adsets_in_campaign(self, fb_campaign_id, logger):
		campaign = Campaign(str(fb_campaign_id))
		try:
			for adset in campaign.get_ad_sets([
				AdSet.Field.id,
				AdSet.Field.name,
				AdSet.Field.status,
			]):
				print 'each adset'
				fb_adset_id = int(adset[AdSet.Field.id])
				print fb_adset_id
				print str(adset[AdSet.Field.status])
				adset = AdSet(str(fb_adset_id))
				#adset.remote_delete()
				adset.update({
					AdSet.Field.status: AdSet.Status.paused,
				})
				print str(adset[AdSet.Field.status])
				adset.remote_update()
		except Exception as e:
			logger.exception(e)

	def delete_adset(self, fb_adset_id, logger):
		try:
			print fb_adset_id
			adset = AdSet(str(fb_adset_id))
			adset.remote_delete()
		except Exception as e:
			logger.exception(e)

	def paused_adset(self, fb_adset_id, logger):
		try:
			print fb_adset_id
			adset = AdSet(str(fb_adset_id))
			adset.update({
				AdSet.Field.status: AdSet.Status.paused,
			})
			print str(adset[AdSet.Field.status])
			adset.remote_update()
		except Exception as e:
			logger.exception(e)

	def delete_adsets_in_campaign(self, fb_campaign_id, logger):
		campaign = Campaign(str(fb_campaign_id))
		try:
			for adset in campaign.get_ad_sets([
				AdSet.Field.id,
				AdSet.Field.name,
				AdSet.Field.status,
			]):
				print 'each adset'
				fb_adset_id = int(adset[AdSet.Field.id])
				print fb_adset_id
				print str(adset[AdSet.Field.status])
				#adset = AdSet(str(fb_adset_id))
				#adset.remote_delete()
		except Exception as e:
			logger.exception(e)

	def query_adset_info(self, logger):
		print 'query_adset_info'
		#account_id = 765120010252743
		account_id = 763181827135742
		account = AdAccount('act_' + str(account_id))
		campaigns = account.get_ad_campaigns(fields=[
			Campaign.Field.id,
			Campaign.Field.name,
			Campaign.Field.status,
			Campaign.Field.is_completed,
		])
		for campaign in campaigns:
			campaign_id = campaign[Campaign.Field.id]
			print campaign_id
			if int(campaign_id) != 6039319134609:
				continue
			print campaign[Campaign.Field.status]
			print 'test'
			for adset in campaign.get_ad_sets([
				AdSet.Field.id,
				AdSet.Field.name,
				AdSet.Field.bid_amount,
			]):
				print 'each adset'
				fb_adset_id = int(adset[AdSet.Field.id])
				name = str(adset[AdSet.Field.name])
				bid_amount = int(adset[AdSet.Field.bid_amount])
				print fb_adset_id, name

	def query_ad_info(self,logger):
		#ad = Ad(str(6034644925448))
		#ad.remote_read(fields=[AdGoup.Field.name])
		#print ad[Ad.Field.id]
		#print ad[Ad.Field.name]
		creative = AdCreative(str(6034644852048))
		creative.remote_read(fields=[
			AdCreative.Field.link_url, 
			AdCreative.Field.id,
			AdCreative.Field.object_url,
			AdCreative.Field.follow_redirect])
		print creative[AdCreative.Field.id]
		print creative[AdCreative.Field.follow_redirect]
		print creative[AdCreative.Field.link_url]
		print creative[AdCreative.Field.object_store_url]

	def get_account_status(self, account_id, logger):
		print 'get account status'
		account = AdAccount('act_'+str(account_id))
		account.remote_read(fields=[
			AdAccount.Field.account_id,
			AdAccount.Field.account_status,
		])
		print account[AdAccount.Field.account_id]
		print account[AdAccount.Field.account_status]

	def get_ads_status_under_campaign(self, campaign_id, logger):
		campaign = Campaign(str(campaign_id))
		print campaign_id
		for adset in campaign.get_ad_groups([
			Ad.Field.id,
			Ad.Field.status,
		]):
			print adset[Ad.Field.id], adset[Ad.Field.status]

	def get_adsets_status_under_campaign(self, campaign_id, logger):
		campaign = Campaign(str(campaign_id))
		print 'campaign', campaign_id
		for adset in campaign.get_ad_sets([
			AdSet.Field.id,
			AdSet.Field.status,
			AdSet.Field.bid_amount,
		]):
			print 'adset', adset[AdSet.Field.id], adset[AdSet.Field.status], adset[AdSet.Field.bid_amount]

	def get_campaign_status(self, campaign_id, logger):
		print 'campaign', campaign_id
		campaign = Campaign(str(campaign_id))
		campaign.remote_read(fields=[
			Campaign.Field.id,
			Campaign.Field.status,
		])
		print 'campaign_status', campaign[Campaign.Field.id], campaign[Campaign.Field.status]

	def get_adset_status(self, adset_id, logger):
		try:
			print 'adset', adset_id
			adset = AdSet(str(adset_id))
			adset.remote_read(fields=[
				AdSet.Field.id,
				AdSet.Field.status,
				AdSet.Field.targeting
			])
			print 'adset_status', adset[AdSet.Field.id], adset[AdSet.Field.status]
			targeting = adset[AdSet.Field.targeting]
			print targeting
			print
			print targeting['age_min']
			print targeting['locales']
			print type(targeting['locales'])
		
		except Exception as e:
			logger.exception(e)

	def get_reach_estimate(self, ad_id, logger):
		ad = Ad(str(ad_id))
		reach_estimate = ad.get_reach_estimate()
		print reach_estimate[0]['users']

	def get_campaign_insight(self, campaign_id, logger):
		campaign = Campaign(str(campaign_id))
		params = {
			'time_range':{'since':'2016-04-18', 'until':'2016-04-18'},
			'level':'campaign_group',
		}
		insights = campaign.get_insights(params=params)
		for insight in insights:
			print insight

	def get_ad_insight(self, ad_id, logger):
		ad = Ad(str(ad_id))
		params = {
			'time_range':{'since':'2016-04-19', 'until':'2016-04-19'},
			'level':'adgroup',
		}
		insights = ad.get_insights(params=params)
		for insight in insights:
			print insight

	def get_account_name(self, fb_account_id, logger):
		account_name = 'unknown_account'
		try:
			account = AdAccount('act_'+str(fb_account_id))
			account.remote_read(fields=[
				AdAccount.Field.account_id,
				AdAccount.Field.name,
			])
			account_name = account[AdAccount.Field.name]
			print account_name
		except Exception as e:
			logger.exception(e)
		finally:
			return account_name

	#def get_adsets_under_account(self, fb_account_id, logger):
	#	try:
	#		account = AdAccount('act_'+str(fb_account_id))
	#		adsets = account.get_ad_sets(fields=[AdSet.Field.promoted_object])
	#		print adsets
	#		print len(adsets)
	#		count = 0
	#		for adset in adsets:
	#			print adset[AdSet.Field.promoted_object]
	#			count += 1
	#		print len(adsets)
	#	except Exception as e:
	#		logger.exception(e)

	def generate_batches(self, iterable, batch_size_limit):
		"""
		Generator that yields lists of length size batch_size_limit containing
		objects yielded by the iterable.
		"""
		batch = []

		for item in iterable:
			if len(batch) == batch_size_limit:
				yield batch
				batch = []
			batch.append(item)

		if len(batch):
			yield batch

	def get_ads_stats(self, fb_account_id, ad_ids, start_dt, end_dt, logger):
		try:
			params = {
				'time_range': { 'since': start_dt, 'until': end_dt },
				'level': 'ad',
				'fields':['spend','social_clicks', 'social_impressions','unique_social_clicks', 'inline_link_clicks', 'impressions', 'actions', 'relevance_score', 'ad_id', 'adset_id', 'campaign_id', 'reach', 'frequency', 'unique_clicks'],

			insights = []
			for ad_id in ad_ids:
				ad = Ad(str(ad_id))
				ad_insight = ad.get_insights(params=params)
				print ad_insight
				insights.append(ad_insight)
			print len(insights)
				
		except Excepion as e:
			logger.exception(e)

	def get_ads_stats(self, fb_account_id, ad_ids, start_dt, end_dt, logger):
		try:
			account = AdAccount("act_" + str(fb_account_id))
			params = {
				'time_range': { 'since': start_dt, 'until': end_dt },
				'level': 'ad',
				'fields':['spend','social_clicks', 'social_impressions','unique_social_clicks', 'inline_link_clicks', 'impressions', 'actions', 'relevance_score', 'ad_id', 'adset_id', 'campaign_id', 'reach', 'frequency', 'unique_clicks'],
			}
			insights_iterator = account.get_insights(params=params)

			AD_BATCH_LIMIT = 25

			# Iterate over batches of active AdCampaign's
			total_insights = []
			count = 0
			for ads_insight in self.generate_batches(
				insights_iterator,
				AD_BATCH_LIMIT,
			):
				api_batch = self.api.new_batch()

				print 'count', count, len(ads_insight)
				for ad_insight in ads_insight:
					print ad_insight['ad_id'], ad_insight['adset_id'], ad_insight['campaign_id'], ad_insight['impressions']
				total_insights.extend(ads_insight)
				api_batch.execute()

			print 'total_insights', len(total_insights)

		except Exception as e:
			logger.exception(e)

	def get_adsets_info(self, fb_adset_ids, logger):
		adset_info = []
		
		api_batch = self.api.new_batch()
		count = 0

		from functools import partial
		for fb_adset_id in fb_adset_ids:
			adset = AdSet(str(fb_adset_id))
			count = count + 1

			adset.read(fields=[
				AdSet.Field.id,
				AdSet.Field.campaign_id,
				AdSet.Field.bid_amount,
				AdSet.Field.is_autobid,
				AdSet.Field.targeting,
				AdSet.Field.billing_event,
				AdSet.Field.optimization_goal,
			])
			def callback_success(response, my_adset=None, adset_info = []):
				adset_info.append(my_adset)
			callback_success = partial(
				callback_success,
				my_adset=adset,
				adset_info=adset_info
			)
			adset.remote_read(
				batch=api_batch,
				success=callback_success)
				
			if count >= 25:
				api_batch.execute()
				api_batch = self.api.new_batch()
				count = 0
		
		api_batch.execute()
		print adset_info

	def get_adsets_under_account(self, fb_account_id, logger):
		total_adsets = []
		try:
			account = AdAccount('act_'+str(fb_account_id))

			related_adsets_iterator = account.get_ad_sets(
				fields=[
					AdSet.Field.status,
					AdSet.Field.name,
					AdSet.Field.id,
				],
				params={
					#AdSet.Field.status: [AdSet.Status.active],
					AdSet.Field.id: [6041816621449],
				}
			)
			ADSET_BATCH_LIMIT = 25

			# Iterate over batches of active AdCampaign's
			count = 0
			for adsets in self.generate_batches(
				related_adsets_iterator,
				ADSET_BATCH_LIMIT,
			):
				api_batch = self.api.new_batch()

				print 'count', count, len(adsets)
				print adsets
				total_adsets.extend(adsets)

				if len(total_adsets) > 100:
					print 'enough adsets for test'
					break

				#for my_adset in adsets:

				#	def callback_success(response, my_adset=None):
				#		print(
				#			"Operated on %s successfully."
				#			% my_adset[AdCampaign.Field.id]
				#		)
				#	callback_success = partial(
				#		callback_success,
				#		my_adset=my_adset,
				#	)

				#	def callback_failure(response, my_adset=None):
				#		print(
				#			"Operated on %s failed"
				#			% my_adset[AdCampaign.Field.id]
				#		)
				#		raise response.error()
				#	callback_failure = partial(
				#		callback_failure,
				#		my_adset=my_adset,
				#	)

				#	my_adset.remote_read(
				#		batch=api_batch,
				#		success=callback_success,
				#		failure=callback_failure,
				#	)

				api_batch.execute()

			print 'total_adsets', len(total_adsets)
			return total_adsets

		except Exception as e:
			logger.exception(e)

	def get_creative_under_ad(self, fb_ad_id, logger):
		ad = Ad(str(fb_ad_id))
		creatives = ad.get_ad_creatives()
		print creatives


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
		#TestManager(conf).update_creative_text(6042021453485, 6042021441485, logger)
		#TestManager(conf).run(logger)	
		#TestManager(conf).query_adset_info(logger)
		#TestManager(conf).query_info(logger)
		#TestManager(conf).query_ad_info(logger)
		#TestManager(conf).delete_campaign(logger)
		#TestManager(conf).get_stats(logger)	
		#TestManager(conf).get_account_info(logger)
		#test_account_id = 794200410678036
		#test_campaign_ids = [6034371979411, 6034372150011, 6034372366011, 6034372391411, 6034372401211, 6034372447611, 6034372583211, 6034372765811, 6034372916211, 6034372965411, 6034373157411]
		#test_account_id = 518371891677974
		#test_campaign_ids = [6034048658303, 6034060245503, 6034079787903, 6034087732103]
		#test_account_id = 914946688625921
		#test_campaign_ids = [6037317183433]
		##test_account_id = 0
		##test_campaign_ids = [ 6038742117716 ]
		#test_campaign_ids = [ 6044089017804 ]
		#test_dt = '2016-04-27'
		#for test_campaign_id in test_campaign_ids:
		#	try:
		#		TestManager(conf).get_campaign_stats(test_campaign_id, test_dt, logger)	
		#	except Exception, e:
		#		print e
		#TestManager(conf).create_lookalike_audience(logger)
		#for i in range(1):
		#	TestManager(conf).create_ad_account(logger)	
		#test_campaign_ids = [6036846342685, 6036846611485, 6036855643685]
		#[ TestManager(conf).query_campaign_info(test_campaign_id, logger) for test_campaign_id in test_campaign_ids ]	
		#test_account_id = 518371845011312
		#test_account_id = 515737275274769
		#test_account_id = 851961091571148 
		#TestManager(conf).get_account_status(test_account_id, logger)

		## account spend
		#test_account_id = 830299807068096
		#start_dt = '20160401'
		#end_dt = '20160509'
		#start_dt_d = datetime.datetime.strptime(str(start_dt), '%Y%m%d')
		#end_dt_d = datetime.datetime.strptime(str(end_dt), '%Y%m%d')
		#day_count = (end_dt_d - start_dt_d).days + 1
		#account_stats_list = []
		#for cur_dt_d in (start_dt_d + datetime.timedelta(n) for n in range(day_count)):
		#	cur_dt = str(cur_dt_d.strftime('%Y-%m-%d'))
		#	print cur_dt
		#	account_stats = TestManager(conf).get_account_stats(test_account_id, cur_dt, cur_dt, logger)
		#	account_stats_list.append(account_stats)
		#df = pd.DataFrame(account_stats_list)
		#print df
		#df.to_csv('for_renjie.csv')
		
		#TestManager(conf).query_campaign_info(6038742117716, logger)
		#delete_campaign_ids = [6038079661519, 6038591807204, 6038591940804, 6038592426004, 6038595946004, 6038595999604, 6038596020404, 6047052119580, 6047052581580, 6047052682180, 6047053141580, 6047053248980, 6038086142319]
		#for delete_campaign_id in delete_campaign_ids:
		#	TestManager(conf).query_campaign_info(delete_campaign_id, logger)
		#	#TestManager(conf).delete_campaign(delete_campaign_id, logger)
		#TestManager(conf).get_ads_status_under_campaign(6045103309719, logger)
		#TestManager(conf).get_ads_status_under_campaign(6044467830713, logger)
		#campaign_ids = [6043186175135,6043186291935,6043227901135,6043227968135,6043287326535,6043287512535,6043369292535,6043369424935]
		#for campaign_id in campaign_ids:
		#	TestManager(conf).get_adsets_status_under_campaign(campaign_id, logger)
		#test_account_id = 516522181862945
		#TestManager(conf).get_adsets_under_account(test_account_id, logger)
		test_adset_ids = [ "6041816621449", "6041816621649","6041816621849"]
		TestManager(conf).get_adsets_info(test_adset_ids, logger)
		#TestManager(conf).get_ads_stats(test_account_id, [], '2016-07-07', '2016-07-07', logger)
		#TestManager(conf).get_ads_stats(test_account_id, [], '2016-07-01', '2016-07-01', logger)
		#TestManager(conf).get_campaign_status(6051178085866, logger)
		#TestManager(conf).get_creative_under_ad(6048351879242, logger)
		#test_adset_ids = [6049834687009, 6049834683209, 6049834686609, 6049834677809, 6049834675809, 6049834686809, 6049834691009, 6049834682809, 6049834677609, 6049834690209, 6049834694809, 6049834699209, 6049834699809, 6049834695409, 6049834701809, 6049834695009]        
		#test_adset_ids = [6042283799716,6040000885024,6043017290663,6043017330063,6043017290863,6043017305863,6043017329863,6043017317663,6043017304863,6043017330263,6043017318463,6043017330463,6043017291063,6043017304663,6043017290463,6043017330663,6043017291263,6043017318063,6043017305463,6043017304263,6043017317263,6043017317863,6043017342463,6043017342263,6043017341863,6043017341663,6043017341463,6043017348663,6040660144285,6040660143885,6040318436824]
		#test_adset_ids = [6039516567408,6039516610408,6039585052208,6039585264808,6039585316008,6040134897808,6040134898608,6040134950208,6040134950008,6040135096008,6040137235608,6040137254608,6040137254408,6040149211208,6040149210408,6040149253008,6040149253208,6040214146408,6040271471808,6040279597608,6040280706808,6040280707608]
		#for test_adset_id in test_adset_ids:
		#	TestManager(conf).paused_adset(test_adset_id, logger)
		#	TestManager(conf).get_adset_status(test_adset_id, logger)

		#TestManager(conf).get_adset_status(6055298930209, logger)
		#TestManager(conf).get_adset_status(6054710999409, logger)
		#TestManager(conf).get_adset_status(6055299246209, logger)

		#delete_adset_ids = [6040214147208,6040271472608,6040280709008,6040280708608]
		#for delete_adset_id in delete_adset_ids:
		#	TestManager(conf).delete_adset(delete_adset_id, logger)
		#	TestManager(conf).get_adset_status(delete_adset_id, logger)
			
		#TestManager(conf).pause_adsets_in_campaign(6042682279566, logger)
		#test_ad_ids = [6041016059804, 6041016062004, 6041016059604, 6041016061804, 6041016062204]
		#test_ad_ids = [6044659510719]
		##test_ad_ids = [6043691774604, 6044501815204, 6044501810804]
		#for ad_id in test_ad_ids:
		#	print 'ad_id', ad_id
		#	TestManager(conf).get_ad_insight(ad_id, logger)
		#	TestManager(conf).get_reach_estimate(ad_id, logger)
		#campaign_id = 6043691766004 
		#TestManager(conf).get_campaign_insight(campaign_id, logger)
		#now = time.localtime()
		#account_id = 914946688625921
		#TestManager(conf).get_yesterday_stats(account_id, now, logger)
		#test_account_id = 830299530401457
		#TestManager(conf).get_account_name(test_account_id, logger)
	except Exception,e:
		logging.exception(e)


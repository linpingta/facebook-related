# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

import unittest

from basic import BasicManager, BasicManagerTest
from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	AdSet,
)


class AdSetManager(BasicManager):

	def __init__(self, conf):
		super(AdSetManager, self).__init__(conf)

	def create_adset(self, fb_account_id, fb_campaign_id, logger):
		try:
			bid_amount = 100 # means 100 cent
		
			# now
			cur_time = int(time.time())
			begin_time = cur_time
			end_time = cur_time + 360000

			# promoted info
			promoted_object = {
				"object_store_url": 'YOUR_OBJECT_STORE_URL', "application_id": 'YOUR_APPLICATION_ID'
			}

			# oCPM case
			billing_event = AdSet.BillingEvent.impressions
			optimization_goal = AdSet.OptimizationGoal.app_installs
			
			# targeting IOS example
			adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["mobilefeed"], "user_os": ["iOS_ver_6.0_and_above"], "age_min": "28", "genders": [1]}
			# targeting Android example
			#adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["mobilefeed"], "user_os": ["Android_ver_2.3_and_above"], "age_min": "28", "genders": [1]}

			# adset create
			ad_set = AdSet(parent_id='act_' + str(fb_account_id))
			ad_set.update({
				AdSet.Field.name: 'video_test_5_adset',
				AdSet.Field.status: AdSet.Status.active,
				AdSet.Field.bid_amount: bid_amount,
				AdSet.Field.billing_event : billing_event,
				AdSet.Field.optimization_goal : optimization_goal,
				AdSet.Field.promoted_object: json.dumps(promoted_object),
				AdSet.Field.daily_budget: '1000',
				AdSet.Field.created_time: str(cur_time),
				AdSet.Field.start_time: str(begin_time),
				AdSet.Field.end_time: str(end_time),
				AdSet.Field.campaign_group_id: str(fb_campaign_id),
				AdSet.Field.targeting: json.dumps(adset_target_dict)
			})
			ad_set.remote_create()
		except Exception as e:
			logger.exception(e)

	def create_adsets(self, now, logger):
		error_reasons = []
		adset_infos = []
		adset_error_infos = []
		try:
			api_batch = self.api.new_batch()

			bid_amount = 100 # means 100 cent
		
			# now
			cur_time = int(time.time())
			begin_time = cur_time
			end_time = cur_time + 360000

			# promoted info
			promoted_object = {
				"object_store_url": 'YOUR_OBJECT_STORE_URL', "application_id": 'YOUR_APPLICATION_ID'
			}

			# oCPM case
			billing_event = AdSet.BillingEvent.impressions
			optimization_goal = AdSet.OptimizationGoal.app_installs
			
			# targeting IOS example
			adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["mobilefeed"], "user_os": ["iOS_ver_6.0_and_above"], "age_min": "28", "genders": [1]}
			# targeting Android example
			#adset_target_dict = {"geo_locations": {"countries": ["US"]}, "age_max": "42", "page_types": ["mobilefeed"], "user_os": ["Android_ver_2.3_and_above"], "age_min": "28", "genders": [1]}

			def callback_success(response, adset_info = []):
				''' nothing to do for success'''
				pass

			def callback_failure(response, adset_info = [], error_reasons = [], adset_error_infos = []):
				''' add adset_id to fail_list'''
				error_info_dict = {}
				response_error = response.error()
				error_info_dict['body']= response_error.body()
				try:
					error_user_msg = error_info_dict['body']['error']['error_user_msg']
				except Exception as e:
					error_reasons.append(error_info_dict)
				else:
					error_reasons.append(error_user_msg)
				adset_error_infos.append(adset_info)

			count = 0
			MAX_ADSET_NUM_PER_BATCH = 25
			for i in range(100):
				
				callback_failure = partial(
					callback_failure,
					adset_info = adset_info,
					error_reasons = error_reasons,
					adset_error_infos = adset_error_infos,
				)
				callback_success = partial(
					callback_success,
					adset_info = adset_info,
				)

				ad_set.update({
					AdSet.Field.name: 'adset %d' % i,
					AdSet.Field.status: AdSet.Status.active,
					AdSet.Field.billing_event: billing_event,
					AdSet.Field.optimization_goal: optimization_goal,
					AdSet.Field.bid_amount: bid_amount,
					AdSet.Field.promoted_object: promoted_object,
					AdSet.Field.lifetime_budget: str(10000),
					AdSet.Field.created_time: str(cur_time),
					AdSet.Field.start_time: str(begin_time),
					AdSet.Field.end_time: str(end_time),
					AdSet.Field.campaign_id: str(fb_campaign_id),
					AdSet.Field.targeting: json.dumps(adset_target_dict)
				})
				ad_set.remote_create(batch=api_batch, success=callback_success, failure=callback_failure,)

				count = count + 1
				if count > MAX_ADSET_NUM_PER_BATCH:
					api_batch.execute()
					api_batch = self.api.new_batch()
					count = 0
			api_batch.execute()

		except Exception as e:
			logger.exception(e)

	def delete_adset(self, fb_adset_id, logger):
		''' delete adset'''
		try:
			logger.debug('delete fb_adset_id %d' % fb_adset_id)
			if fb_adset_id > 0:
				adset = AdSet(str(fb_adset_id))
				adset.remote_delete()
		except Exception as e:
			logger.exception(e)

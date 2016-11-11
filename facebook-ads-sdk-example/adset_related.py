# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	AdAccount,
	Campaign,
	AdSet,
	TargetingSpecsField,
)
from basic import APIManager


class AdSetManager(APIManager):

	def __init__(self, conf):
		super(AdSetManager, self).__init__(conf)

	def create_adset(self, fb_account_id, fb_campaign_id, logger):
		""" create adset
		Please update promoted_object, billing_event/optimization_goal, targeting as you needed
		"""
		try:
			bid_amount = 100 # means 100 cent, 1 dollar
			daily_budget = 1000 # means 10 dollars most spent every day
			# is_autbid decide whether to use autobid
		
			# now
			cur_time = int(time.time())
			begin_time = cur_time
			end_time = cur_time + 360000

			# promoted info
			# you must promise object store url is the same type as user_os
			promoted_object = {
				"object_store_url": 'YOUR_OBJECT_STORE_URL', "application_id": 'YOUR_APPLICATION_ID'
			}

			# oCPM case
			# other type as CPM, CPC, CPA, change billing_event , or optimization_goal
			billing_event = AdSet.BillingEvent.impressions
			optimization_goal = AdSet.OptimizationGoal.app_installs
			
			# targeting IOS example
			adset_target_dict = {
				"geo_locations": {"countries": ["US"]}, 
				"age_max": "42", 
				"page_types": ["mobilefeed"], 
				"user_os": ["iOS_ver_6.0_and_above"], 
				"age_min": "28", 
				"genders": [1]
			}

			# targeting Android example
			adset_target_dict = {
				"geo_locations": {"countries": ["US"]}, 
				"age_max": "42", 
				"page_types": ["mobilefeed"], 
				"user_os": ["Android_ver_2.3_and_above"],
				"age_min": "28", 
				"genders": [1]
			}

			# adset create
			ad_set = AdSet(parent_id='act_' + str(fb_account_id))
			ad_set.update({
				AdSet.Field.name: 'adset_test',
				AdSet.Field.status: AdSet.Status.active,
				AdSet.Field.bid_amount: bid_amount,
				AdSet.Field.billing_event : billing_event,
				AdSet.Field.optimization_goal : optimization_goal,
				AdSet.Field.promoted_object: json.dumps(promoted_object),
				AdSet.Field.daily_budget: str(daily_budget),
				AdSet.Field.created_time: str(cur_time),
				AdSet.Field.start_time: str(begin_time),
				#AdSet.Field.end_time: str(end_time),		# not necessary if no end time need in business		
				AdSet.Field.campaign_group_id: str(fb_campaign_id),  # decide which campaign to created in
				AdSet.Field.targeting: json.dumps(adset_target_dict)
			})
			ad_set.remote_create()
			return int(ad_set[AdSet.Field.id])

		except Exception as e:
			logger.exception(e)

	def create_adsets(self, fb_account_id, fb_campaign_id, logger):
		""" Create multi-adsets with batch API"""
		error_reasons = []
		adset_infos = []
		adset_error_infos = []
		try:
			api_batch = self.api.new_batch()

			bid_amount = 100 # means 100 cent
			daily_budget = 1000 # means 10 dollars most spent every day
			# is_autbid decide whether to use autobid
		
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
			adset_target_dict = {
				"geo_locations": {"countries": ["US"]}, 
				"age_max": "42", 
				"page_types": ["mobilefeed"], 
				"user_os": ["iOS_ver_6.0_and_above"], 
				"age_min": "28", 
				"genders": [1]
			}

			# targeting Android example
			adset_target_dict = {
				"geo_locations": {"countries": ["US"]}, 
				"age_max": "42", 
				"page_types": ["mobilefeed"], 
				"user_os": ["Android_ver_2.3_and_above"],
				"age_min": "28", 
				"genders": [1]
			}

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
				except KeyErro as e:
					error_reasons.append(error_info_dict)
				else:
					error_reasons.append(error_user_msg)
				adset_error_infos.append(adset_info)

			count = 0
			MAX_ADSET_NUM_PER_BATCH = 25
			for i in range(100):
				
				ad_set = AdSet(parent_id='act_' + str(fb_account_id))

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
					AdSet.Field.lifetime_budget: str(daily_budget),
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
		""" delete adset"""
		try:
			logger.debug('delete fb_adset_id %d' % fb_adset_id)
			if fb_adset_id > 0:
				adset = AdSet(str(fb_adset_id))
				adset.remote_delete()

		except Exception as e:
			logger.exception(e)

	def update_adset_status(self, fb_adset_id, status, logger):
		try:
			# status = AdSet.Status.paused
			print fb_adset_id
			adset = AdSet(str(fb_adset_id))
			adset.update({
				AdSet.Field.status: status,
			})
			adset.remote_update()

		except Exception as e:
			logger.exception(e)

	def get_adset_status(self, fb_adset_id, logger):
		try:
			print fb_adset_id
			adset = AdSet(str(fb_adset_id))
			adset.remote_read(fields=[
				AdSet.Field.id,
				AdSet.Field.status,
				AdSet.Field.targeting
			])
			print 'adset_status', adset[AdSet.Field.id], adset[AdSet.Field.status]

		except Exception as e:
			logger.exception(e)

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
					AdSet.Field.status: [AdSet.Status.active],
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

				api_batch.execute()

			print 'total_adsets', len(total_adsets)
			return total_adsets

		except Exception as e:
			logger.exception(e)

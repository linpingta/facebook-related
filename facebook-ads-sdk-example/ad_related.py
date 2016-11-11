# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	AdAccount,
	Campaign,
	AdSet,
	Ad,
	TargetingSpecsField,
)
from basic import APIManager


class AdManager(APIManager):

	def __init__(self, conf):
		super(AdManager, self).__init__(conf)

	def create_ad(self, fb_account_id, fb_adset_id, fb_creative_id, logger):
		""" create ad"""
		try:
			ad = Ad(parent_id='act_' + str(fb_account_id))
			ad.update({
				Ad.Field.name: 'test_ad',
				Ad.Field.status: Ad.Status.active,
				Ad.Field.adset_id: fb_adset_id,
				Ad.Field.creative: {
					Ad.Field.Creative.creative_id: fb_creative_id,
				},
			})
			ad.remote_create()

		except Exception as e:
			logger.exception(e)

	def create_ads(self, fb_account_id, fb_adset_id, fb_creative_id, logger):
		""" create multi ads in one adset with one creative"""
		error_reasons = []
		ad_infos = []
		ad_error_infos = []
		try:
			api_batch = self.api.new_batch()

			def callback_success(response, ad_info = []):
				''' nothing to do for success'''
				pass

			def callback_failure(response, ad_info = [], error_reasons = [], ad_error_infos = []):
				''' add ad_id to fail_list'''
				error_info_dict = {}
				response_error = response.error()
				error_info_dict['body']= response_error.body()
				try:
					error_user_msg = error_info_dict['body']['error']['error_user_msg']
				except Exception as e:
					error_reasons.append(error_info_dict)
				else:
					error_reasons.append(error_user_msg)
				ad_error_infos.append(ad_info)

			count = 0
			MAX_ADSET_NUM_PER_BATCH = 25
			for i in range(100):
				
				callback_failure = partial(
					callback_failure,
					ad_info = ad_info,
					error_reasons = error_reasons,
					ad_error_infos = ad_error_infos,
				)
				callback_success = partial(
					callback_success,
					ad_info = ad_info,
				)

				ad = Ad(parent_id='act_' + str(fb_account_id))
				ad.update({
					Ad.Field.name: 'test_ad',
					Ad.Field.status: Ad.Status.active,
					Ad.Field.ad_id: fb_ad_id,
					Ad.Field.creative: {
						Ad.Field.Creative.creative_id: fb_creative_id,
					},
				})
				ad.remote_create(batch=api_batch, success=callback_success, failure=callback_failure,)

				count = count + 1
				if count > MAX_ADSET_NUM_PER_BATCH:
					api_batch.execute()
					api_batch = self.api.new_batch()
					count = 0
			api_batch.execute()

		except Exception as e:
			logger.exception(e)

	def delete_ad(self, fb_ad_id, logger):
		""" delete ad"""
		try:
			logger.debug('delete fb_ad_id %d' % fb_ad_id)
			if fb_ad_id > 0:
				ad = Ad(str(fb_ad_id))
				ad.remote_delete()

		except Exception as e:
			logger.exception(e)

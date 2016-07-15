# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

import unittest

from basic import BasicManager, BasicManagerTest
from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	AdAccount,
	Campaign,
	AdSet,
	Ad,
)


class InsightManager(BasicManager):

	def __init__(self, conf):
		super(CampaignManager, self).__init__(conf)

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

	def get_campaign_insight(self, campaign_id, start_dt, end_dt,logger):
		campaign = Campaign(str(campaign_id))
		params = {
			'time_range':{'since':str(start_dt), 'until':str(end_dt)},
			'level':'campaign_group',
		}
		insights = campaign.get_insights(params=params)
		for insight in insights:
			print insight

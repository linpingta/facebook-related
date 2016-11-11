# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :


from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	AdAccount,
	Campaign,
	AdSet,
	Ad,
)
from basic import APIManager


class InsightManager(APIManager):
	""" Insight Manager
	"""
	def __init__(self, conf):
		super(InsightManager, self).__init__(conf)

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

	def get_campaign_insight(self, fb_campaign_id, start_dt, end_dt,logger):
		campaign = Campaign(str(fb_campaign_id))
		params = {
			'time_range':{'since':str(start_dt), 'until':str(end_dt)},
			'level':'campaign',
		}
		insights = campaign.get_insights(params=params)
		for insight in insights:
			print insight

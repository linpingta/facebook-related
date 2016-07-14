# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

import unittest

from basic import BasicManager, BasicManagerTest
from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	Campaign,
)


class CampaignManager(BasicManager):

	def __init__(self, conf):
		super(CampaignManager, self).__init__(conf)

	def create_campaign(self, fb_account_id, logger):
		try:
			campaign = Campaign(parent_id='act_' + str(zeus_campaign.fb_account_id))
			campaign.update({
				Campaign.Field.name: 'created_campaign',
				Campaign.Field.objective: Campaign.Objective.mobile_app_installs,
				Campaign.Field.status: Campaign.Status.paused,
				Campaign.Field.buying_type: Campaign.BuyingType.auction,
			})
			campaign.remote_create()
		except Exception as e:
			logger.exception(e)

	def update_campaign(self, fb_campaign_id, logger):
		''' update fb campaign'''
		try:
			campaign = Campaign(str(fb_campaign_id))
			campaign.remote_read(fields=[
				Campaign.Field.id,
				Campaign.Field.status,
			])
			if campaign[Campaign.Field.status] == 'ARCHIVED':
				logger.error('cpid[%d] in ARCHIVED status, no update' % fb_campaign_id)
				return

			campaign.update({
				Campaign.Field.name: 'update_campaign',
			})
			campaign.remote_update()
		except Exception as e:
			logger.exception(e)

	def delete_campaign(self, fb_campaign_id, logger):
		''' delte fb campaign'''
		try:
			if fb_campaign_id > 0:
				campaign = Campaign(str(fb_campaign_id))
				campaign.remote_delete()
				logger.warning('fb_cpid[%d] deleted' % fb_campaign_id)
			else:
				logger.warning('fb_cpid[%d] invalid for fb delete' % fb_campaign_id)
		except Exception as e:
			logger.exception(e)

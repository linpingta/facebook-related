# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :


from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData, VideoData
from facebookads.objects import (
	AdAccount,
	Campaign,
	AdSet,
)
from basic import APIManager


class CampaignManager(APIManager):
	""" Campaign Related Usage
	"""
	def __init__(self, conf):
		super(CampaignManager, self).__init__(conf)

	def create_campaign(self, fb_account_id, logger):
		""" You must create campaign under one fb_account"""
		try:
			campaign = Campaign(parent_id='act_' + str(fb_account_id))
			campaign.update({
				Campaign.Field.name: 'my_test_campaign',
				# for mobile app install ads
				Campaign.Field.objective: Campaign.Objective.mobile_app_installs,
				## for website conversion ads
				#Campaign.Field.objective: Campaign.Objective.website_clicks,
				Campaign.Field.status: Campaign.Status.paused,
				Campaign.Field.buying_type: Campaign.BuyingType.auction,
			})
			campaign.remote_create()
			return int(campaign[Campaign.Field.id])

		except Exception as e:
			logger.exception(e)

	def update_campaign_name(self, fb_campaign_id, new_campaign_name, logger):
		""" Update fb campaign"""
		try:
			campaign = Campaign(str(fb_campaign_id))

			# You may read campaign field first, not necessary
			campaign.remote_read(fields=[
				Campaign.Field.id,
				Campaign.Field.status,
			])
			if campaign[Campaign.Field.status] == 'ARCHIVED':
				logger.error('cpid[%d] in ARCHIVED status, no update' % fb_campaign_id)
				return

			campaign.update({
				Campaign.Field.name: new_campaign_name,
			})
			campaign.remote_update()

		except Exception as e:
			logger.exception(e)

	def delete_campaign(self, fb_campaign_id, logger):
		""" delte fb campaign"""
		try:
			if fb_campaign_id > 0:
				campaign = Campaign(str(fb_campaign_id))
				campaign.remote_delete()
				logger.warning('fb_cpid[%d] deleted' % fb_campaign_id)
			else:
				logger.warning('fb_cpid[%d] invalid for fb delete' % fb_campaign_id)

		except Exception as e:
			logger.exception(e)

	def read_campaign(self, fb_campaign_id, logger):
		""" read fb campaign"""
		try:
			campaign = Campaign(str(fb_campaign_id))
			campaign.remote_read(fields=[
				Campaign.Field.id,
				Campaign.Field.name,
				Campaign.Field.status,
			])
			# You could only visit fields you ased in remote_read
			print 'campaign info'
			print campaign[Campaign.Field.id]
			print campaign[Campaign.Field.name]
			print campaign[Campaign.Field.status]

		except Exception as e:
			logger.exception(e)

	def get_adsets_under_campaign(self, fb_campaign_id, logger):
		""" read all adset under campaign"""
		total_adsets = []
		try:
			campaign = Campaign(str(fb_campaign_id))

			related_adsets_iterator = campaign.get_ad_sets(
				fields=[
					AdSet.Field.id,
					AdSet.Field.status,
					AdSet.Field.name,
					AdSet.Field.bid_amount,
					AdSet.Field.targeting,
				],
			)
			ADSET_BATCH_LIMIT = 25

			# Iterate over batches of active AdCampaign's
			count = 0
			for adsets in self.generate_batches(
				related_adsets_iterator,
				ADSET_BATCH_LIMIT,
			):
				api_batch = self.api.new_batch()
				total_adsets.extend(adsets)

				if len(total_adsets) >= 4 * ADSET_BATCH_LIMIT: # only fetch most 100 adsets
					break

			return total_adsets

		except Exception as e:
			logger.exception(e)


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

	cm = CampaignManager(conf)

	# input test account 
	# make sure your access_token has CRUD right in test account
	test_account_id = 123456789

	# create campaign
	fb_campaign_id = cm.create_campaign(test_account_id, logger)

	# update campaign
	new_campaign_name = "updated_test_campaign"
	cm.update_campaign_name(fb_campaign_id, new_campaign_name, logger)

	# read campaign
	cm.read_campaign(fb_campaign_id, logger)

	# read adsets under campaign
	cm.get_adsets_under_campaign(fb_campaign_id, logger)

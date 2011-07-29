# Copyright 2011, Global Enterprise and Initiative Group, LLC, and
# Michael Pacchioli.
# 
# This file is part of DeepTweet.
#
# DeepTweet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 3,
# as published by the Free Software Foundation.
#
# DeepTweet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DeepTweet.  If not, see <http://www.gnu.org/licenses/>.



from dt.core.models import Tweet, ProcessedTweet
import datetime, logging

try:
	log
except NameError:
	log = logging.getLogger('dt')



class TweetHandler:

	def __init__(self):
		self.tweet = None
		self.new_tweet = None



	# Don't override this unless making fundamental changes to the system.
	#
	# TODO: Better detection of why Tweet saving can fail.

	def save_new_tweet(self, data, modifier, radius, item, item_spelling):
		self.tweet = Tweet()
		
		self.set_new_tweet_targets()
		
		self.tweet.item = item
		self.tweet.item_spelling = item_spelling

		if len(modifier) > 0:
			self.tweet.modifier = modifier
		else:
			self.tweet.modifier = 'None'

		self.tweet.radius = item.radius

		self.tweet.twitter_id = data.id
		self.tweet.twitter_date = data.created_at
		self.tweet.twitter_user = data.user.screen_name
		self.tweet.text = data.text

		try:
			self.tweet.save()
		except:
			log.error('ERROR SAVING NEW TWEET')



	# Override when adding using different or additional targets.

	def set_new_tweet_targets(self):
		self.tweet.target = None
		self.tweet.target_spelling = None



	# Don't use self.tweet here, use as static function.
	# Override if using different or additional Targets.

	# When adding a new target type, you probably want to
	# make a new function set_x_target, where x is the new
	# Target type name.

	def set_word_target(self, tweet, target, target_spelling):
		tweet.target = target
		tweet.target_spelling = target_spelling

		tweet.date_matched = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		tweet.approved = True

		try:
			tweet.save()
			result = True
		except:
			log.error('ERROR UPDATING TWEET %d WITH WORD TARGET' % (tweet.id))
			result = False

		return result



	# Don't override unless making fundamental changes to the system.
	#
	# TODO: Better way of cloning Tweets?

	def move_tweet(self, tweet):
		log.info('MOVING TWEET %d' % (tweet.id));
		
		self.tweet = tweet
		self.tweet_clone = ProcessedTweet()

		self.set_clone_targets()

		self.tweet_clone.item = tweet.item
		self.tweet_clone.item_spelling = tweet.item_spelling

		self.tweet_clone.modifier = tweet.modifier
		self.tweet_clone.radius = tweet.radius

		self.tweet_clone.twitter_id = tweet.twitter_id
		self.tweet_clone.twitter_date = tweet.twitter_date
		self.tweet_clone.twitter_user = tweet.twitter_user
		self.tweet_clone.text = tweet.text

		self.tweet_clone.date_matched = tweet.date_matched
		self.tweet_clone.approved = tweet.approved

		self.tweet_clone.notes = tweet.notes

		success = True

		try:
				self.tweet_clone.save()
				log.info('CLONED TWEET %d' % (tweet.id))
		except:
				log.error('ERROR MOVING TWEET %d' % (tweet.id))
				success = False

		if success:
			tweet_id = self.tweet.id

			try:
				self.tweet.delete()
				log.info('DELETED OLD TWEET %d' % (tweet_id))
			except:
				log.error('ERROR DELETING OLD TWEET %d' % (tweet_id))
				success = False

		return success



	# Override when adding using different or additional targets.

	def set_clone_targets(self):
		self.tweet_clone.target = self.tweet.target
		self.tweet_clone.target_spelling = self.tweet_clone.target_spelling

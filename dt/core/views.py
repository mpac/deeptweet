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



from django.core.context_processors import request
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from models import \
	Item, ItemSpelling, Tweet, ProcessedTweet, \
	SearchLog, Target, TargetSpelling

from dt.dtlib import TweetHandler
handler = TweetHandler()

import logging
log = logging.getLogger('dt')

import twitter
api = twitter.Api()



def harvest(request):
	items = Item.objects.all()

	for item in items:
		search(item)

	return render_to_response(
		'core/harvest.html',
		{ },
		context_instance = RequestContext(request)
	)



# TODO: Get additional pages of Tweets if 100 or more are retrieved.
# Uniqueness of twitter_id column should handle page overlap.
#
# TODO: Unencode HTML entities in Tweet text.
#
# TODO: Save Tweet geographic information.

def search(item):
	spellings = ItemSpelling.objects.filter(item = item.id, item__active = True)

	modifiers = eval(item.modifier.data)
	radius = eval(item.radius.data)

	log.debug('MODIFIERS: ' + ', '.join(modifiers))

	for modifier in modifiers:
		log.debug('MODIFIER: ' + modifier)
		# continue

		for spelling in spellings:			
			if len(modifier):
				search_text = spelling.text + ' ' + modifier
				geocode = ()
			else:
				search_text = spelling.text

				if radius:
					geocode = radius
				else:
					geocode = ()

			log.debug('SEARCH TEXT: ' + search_text)
			log.debug('RADIUS DATA LENGTH: %d' % (len(geocode)))

			search_log = SearchLog.objects.filter(
				item = item.id, spelling = spelling.id, modifier = modifier, radius = item.radius
			).order_by(
				'-last_twitter_id'
			)

			if search_log:
				twitter_since_id = search_log[0].last_twitter_id
			else:
				twitter_since_id = None

			log.debug('SINCE TWEET ID: ' + twitter_since_id)

			search = None
			search_error = False

			try:
				search = api.GetSearch(
					search_text, per_page = 100,
					geocode = geocode, since_id = twitter_since_id
				)
			except:
				search_error = True

			if search_error:
				try:
					search = api.GetSearch(
						search_text, per_page = 100,
						geocode = geocode
					)
				except:
					pass

			if search and len(search) > 0:
				# Save record of search.

				first_search_id = search[len(search) - 1].id
				last_search_id = search[0].id

				log.debug('FIRST TWEET ID: %d' % (first_search_id))
				log.debug('LAST TWEET ID: %d' % (last_search_id))

				search_log = SearchLog()

				search_log.item = item
				search_log.spelling = spelling
				search_log.modifier = modifier
				search_log.radius = item.radius

				search_log.amount = len(search)
				search_log.maximum = 100

				search_log.first_twitter_id = str(first_search_id)
				search_log.last_twitter_id = str(last_search_id)

				search_log.save()

			for s in search:
				# print s
				# continue

				handler.save_new_tweet(s, modifier, radius, item, spelling)



def process(request):

	# Order by position descending so higher priority targets and spellings
	# are evaluated last and will overwrite previous information.
	#
	# This matches Tweets with targets of type "word", currently the only implemented
	# Target type.

	targets = Target.objects.filter(type='word', active=True).order_by('-position')

	for target in targets:
		for spelling in target.targetspelling_set.all().order_by('-position'):
			log.debug('TARGET SPELLING: ' + spelling.text)
			spelling_text = spelling.text.lower()

			tweets = Tweet.search.query(spelling_text)

			if len(tweets):
				log.debug('TWEETS: %d' % (len(tweets)))

				for tweet in tweets:
					handler.set_word_target(tweet, target, spelling)

	matched_tweets = Tweet.objects.filter(approved = True)
	match_count = len(matched_tweets)

	# If desired, run additional processing using new functions you create,
	# for example, regular expression processing.
	#
	# tweets = Tweet.objects.filter(approved = True)
	#
	# for tweet in tweets:
	#	handler.process_patterns(tweet)


	# Move all Tweets to the ProcessedTweet table, whether or not
	# they are approved (matched with Targets).

	tweets = Tweet.objects.all()

	for tweet in tweets:
		handler.move_tweet(tweet)

	return render_to_response(
		'core/process.html',
		{'match_count': match_count},
		context_instance=RequestContext(request)
	)



def show_results(request):
	tweets = ProcessedTweet.objects.filter(approved = True).order_by('id')

	return render_to_response(
		'core/show_results.html',
		{ 'tweets': tweets },
		context_instance = RequestContext(request)
	)

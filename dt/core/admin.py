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



from dt.core.models import \
	Modifier, Radius, Item, ItemSpelling, \
	Tweet, ProcessedTweet, SearchLog, \
	Target, TargetSpelling

from django.contrib import admin



class TweetAdmin(admin.ModelAdmin):
	list_filter = ['item', 'item_spelling', 'modifier', 'radius']



class ProcessedTweetAdmin(admin.ModelAdmin):
	list_filter = ['item', 'item_spelling', 'modifier', 'radius', 'approved']



class ItemSpellingInline(admin.TabularInline):
	model = ItemSpelling
	extra = 5

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ['text']

		return self.readonly_fields



class TargetSpellingInline(admin.TabularInline):
	model = TargetSpelling
	extra = 5



class ItemAdmin(admin.ModelAdmin):
	# inlines = [
	# 	ItemSpellingInline
	# ]

	def get_readonly_fields(self, request, obj=None):
		if obj: # when editing an object
			return ['name', 'modifier', 'radius']

		return self.readonly_fields



class TargetAdmin(admin.ModelAdmin):
	inlines = [
		TargetSpellingInline
	]

	def get_readonly_fields(self, request, obj=None):
		if obj: # when editing an object
			return ['name', 'type', 'info']

		return self.readonly_fields



admin.site.register(Modifier)
admin.site.register(Radius)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(ProcessedTweet, ProcessedTweetAdmin)
admin.site.register(SearchLog)
admin.site.register(Target, TargetAdmin)

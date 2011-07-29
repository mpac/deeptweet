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



from django.db import models
from dt.fields import AddedDateTimeField, ModifiedDateTimeField
from djangosphinx.models import SphinxSearch

class Modifier(models.Model):
	city = models.CharField(max_length=25, blank=True, null=True)
	data = models.TextField()

	def __unicode__(self):
		return self.data



class Radius(models.Model):
	city = models.CharField(max_length=25, blank=True, null=True)
	data = models.TextField()

	class Meta:
		verbose_name_plural = "Radii"

	def __unicode__(self):
		return self.data



class Item(models.Model):
	name = models.CharField(max_length=100)

	modifier = models.ForeignKey(Modifier)
	radius = models.ForeignKey(Radius)	

	date_added = AddedDateTimeField('Date added', editable=False)
	date_modified = ModifiedDateTimeField('Date modified', editable=False)

	active = models.BooleanField()

	def __unicode__(self):
		return self.name



class Target(models.Model):
	name = models.CharField(max_length=100)

	type = models.CharField(max_length=25, blank=False, null=False, default='word')
	position = models.IntegerField()

	info = models.CharField(max_length=250, blank=True, null=True)

	active = models.BooleanField()

	date_added = AddedDateTimeField('Date added', editable=False)
	date_modified = ModifiedDateTimeField('Date modified', editable=False)

	def __unicode__(self):
		return self.name



class AbstractSpelling(models.Model):
	class Meta:
		abstract = True

	text = models.CharField(max_length=100)

	date_added = AddedDateTimeField('Date added', editable=False)
	date_modified = ModifiedDateTimeField('Date modified', editable=False) 	

	def __unicode__(self):
		return self.text



class ItemSpelling(AbstractSpelling):
	item = models.ForeignKey(Item)

	def save(self):
		if self.pk:
			return
		else:
			super(ItemSpelling, self).save()

	def delete(self):
		return

	

class TargetSpelling(AbstractSpelling):
	target = models.ForeignKey(Target)
	position = models.IntegerField()

	def save(self):
		if self.pk:
			return
		else:
			super(TargetSpelling, self).save()

	def delete(self):
		return



class AbstractTweet(models.Model):
	class Meta:
		abstract = True

	item = models.ForeignKey(Item)
	item_spelling = models.ForeignKey(ItemSpelling)
	modifier = models.CharField(max_length=100)
	radius = models.ForeignKey(Radius)

	twitter_id = models.CharField(max_length=50, unique=True)
	twitter_date = models.CharField(max_length=100)
	twitter_user = models.CharField(max_length=100)
	text = models.CharField(max_length=250)

	date_matched = models.DateTimeField(null=True, default=None)

	approved = models.BooleanField(default=False)

	notes = models.TextField()

	date_added = AddedDateTimeField('Date added', editable=False)
	date_modified = ModifiedDateTimeField('Date modified', editable=False)

	def __unicode__(self):
		return self.twitter_id + ': ' + self.text



class Tweet(AbstractTweet):
	target = models.ForeignKey(Target, related_name='t_target', null=True)
	target_spelling = models.ForeignKey(TargetSpelling, related_name='t_target_spelling', null=True)

	search = SphinxSearch(
		index ='tweet_index', 
		weights = {
			'text': 100,
		}
	)



class ProcessedTweet(AbstractTweet):
	target = models.ForeignKey(Target, related_name='pt_target', null=True)
	target_spelling = models.ForeignKey(TargetSpelling, related_name='pt_target_spelling', null=True)	

	def __unicode__(self):
		return self.twitter_id + ': ' + self.text



class SearchLog(models.Model):
	item = models.ForeignKey(Item)
	spelling = models.ForeignKey(ItemSpelling)
	modifier = models.CharField(max_length=100)
	radius = models.ForeignKey(Radius)

	first_twitter_id = models.CharField(max_length=100)
	last_twitter_id = models.CharField(max_length=100)

	amount = models.IntegerField()
	maximum = models.IntegerField()

	date_added = AddedDateTimeField('Date added', editable=False)
	date_modified = ModifiedDateTimeField('Date modified', editable=False) 	

	def __unicode__(self):
		return str(self.id)

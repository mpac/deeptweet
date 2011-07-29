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

# You should have received a copy of the GNU General Public License
# along with DeepTweet.  If not, see <http://www.gnu.org/licenses/>.



ALTER TABLE core_tweet CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE core_processedtweet CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

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



from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    
    (r'^harvest/', 'dt.core.views.harvest'),
	(r'^process/', 'dt.core.views.process'),
	(r'^$', 'dt.core.views.show_results'),
)

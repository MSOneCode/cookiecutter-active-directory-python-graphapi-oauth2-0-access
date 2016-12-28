"""
Definition of urls for AppOnlyServiceForMicrosoftGraph.
"""

from datetime import datetime
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^connect', 'app.views.connect', name='connect'),
    url(r'^disconnect', 'app.views.disconnect', name='disconnect'),
    url(r'^users', 'app.views.users', name='users'),
    url(r'^add_user', 'app.views.add_user', name='add_user'),
    url(r'^edit_user/(.*)', 'app.views.edit_user', name='edit_user'),
    url(r'^del_user/(.+)', 'app.views.del_user', name='del_user'),

)

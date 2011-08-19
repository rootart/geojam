from django.conf.urls.defaults import patterns, include, url

from feeds import CheckinFeed
from models import Checkin

urlpatterns = patterns('core.views',
    url(r'^(?P<adm_id>\d+)\.(?P<extension>(json)|(kml))$', 'adm_details', 
            name='adm-details'),
)

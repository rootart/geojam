from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.dashboard', name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adm/', include('core.urls')),
    #(r'^auth2/', include('djangofoursquare.urls')),
    (r'^auth/', include('fsq.urls')),
    url(r'^checkins/', 'core.views.checkins', name='checkins'),
    url(r'^checkin/$', 'core.views.checkin', name='checkin')
)


if settings.DEBUG:
    urlpatterns += patterns("django.views",
         (r'^media/(?P<path>.*)$', 'static.serve', \
            {'document_root': settings.STATIC_ROOT,
            'show_indexes': True, }),
    )

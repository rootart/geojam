from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('fsq.views',    
    url(r'^auth/$','auth', name='auth'),
    url(r'^logout/$', 'logout_', name='logout'),
    url(r'^return/$', 'return_', name='callback'),
    )

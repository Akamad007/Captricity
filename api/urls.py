from django.conf.urls.defaults import *


urlpatterns = patterns('api.views',
    # Examples:
    url(r'^add/(\w+)/$', 'add'), 
    url(r'^addall/$', 'addall'),  
    url(r'^viewall/$', 'view_all_batches'),  
    url(r'^batch/(\w+)/$', 'view_batch'),    
    url(r'^data/(\w+)/$', 'data'), 
)
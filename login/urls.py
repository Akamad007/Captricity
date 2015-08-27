from django.conf.urls.defaults import *


urlpatterns = patterns('login.views',
    # Examples:
    url(r'^$', 'login'),  
    url(r'^signup/$', 'signup'),  
    url(r'^logout/$', 'logout'),
        
   #  url(r'^$', include('home.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),
)
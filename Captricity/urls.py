from django.conf.urls import patterns, include, url
from Captricity.settings import OUR_APPS, MEDIA_ROOT, STATIC_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Captricity.views.home', name='home'),
    # url(r'^Captricity/', include('Captricity.foo.urls')),
    url(r'^$', include('home.urls')),
    # Uncomment the admin/doc line be    low to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
for apps in OUR_APPS:
    urlpatterns += patterns('',      
     url(r'^'+apps+'/', include(apps+'.urls')),
    )
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT}))

urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': STATIC_ROOT}))
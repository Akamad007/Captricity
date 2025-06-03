from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
]

for app in settings.OUR_APPS:
    urlpatterns.append(path(f'{app}/', include(f'{app}.urls')))

urlpatterns += [
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
]

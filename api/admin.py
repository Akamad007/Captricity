# flake8: noqa
from django.contrib import admin
from api.models import ApiBatch, ApiBatchData, ApiBatchImage

admin.site.register(ApiBatch)
admin.site.register(ApiBatchData)admin.site.register(ApiBatchImage)

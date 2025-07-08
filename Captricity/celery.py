# flake8: noqa
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# Indicate Celery to use the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Captricity.settings")

app = Celery("Captricity")
app.config_from_object("django.conf:settings")
# This line will tell Celery to autodiscover all your tasks.py that are in your app foldersapp.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from __future__ import absolute_import

# Celery app is optional for running tests
try:
    from .celery import app as celery_app
    __all__ = ['celery_app']
except Exception:
    # Celery may not be installed in test environments
    celery_app = None
    __all__ = []

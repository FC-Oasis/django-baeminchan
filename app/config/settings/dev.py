from .base import *

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

WSGI_APPLICATION = 'config.wsgi.dev.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'baeminchan_db',
        'USER': 'yeojin',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

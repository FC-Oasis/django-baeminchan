import subprocess
import sys
from .base import *

secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json'), 'rb'))

if 'runserver' in sys.argv:
    print('NOTICE: using settings.production in runserver state')
    DEBUG = True
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
    ]
else:
    DEBUG = False
    ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

INSTALLED_APPS += [
    'storages',
]

# AWS
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = secrets['AWS_DEFAULT_ACL']
AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = secrets['AWS_S3_SIGNATURE_VERSION']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']

# Media
DEFAULT_FILE_STORAGE = 'config.storages.S3DefaultStorage'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'

WSGI_APPLICATION = 'config.wsgi.production.application'

DATABASES = secrets['DATABASES']

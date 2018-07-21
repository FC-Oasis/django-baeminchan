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

WSGI_APPLICATION = 'config.wsgi.production.application'

DATABASES = secrets['DATABASES']

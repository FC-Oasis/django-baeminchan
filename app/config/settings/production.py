import subprocess
import sys

import raven

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

    # HTTPS 환경에서 Session, CSRF Cookie 사용하도록 설정
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
       See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)

INSTALLED_APPS += [
    'storages',
    'raven.contrib.django.raven_compat',
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

if 'TRAVIS' in os.environ:
    # Test DB for Travis CI
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'PORT': 5432,
            'HOST': 'localhost',
        }
    }
else:
    DATABASES = secrets['DATABASES']

# Log
# /var/log/django 디렉토리가 존재하면 LOG_DIR로 그대로 사용
# 없으면 ROOT_DIR/.log디렉토리를 사용 (없으면 생성)
LOG_DIR = '/var/log/django'
if not os.path.exists(LOG_DIR):
    LOG_DIR = os.path.join(ROOT_DIR, '.log')
    os.makedirs(LOG_DIR, exist_ok=True)

subprocess.call(['chmod', '755', LOG_DIR])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

RAVEN_CONFIG = {
    'dsn': secrets['SENTRY_DSN'],
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}

CELERY_BROKER_URL = 'redis://' + secrets['AWS_ELASTI_CACHE']
CELERY_RESULT_BACKEND = 'redis://' + secrets['AWS_ELASTI_CACHE']

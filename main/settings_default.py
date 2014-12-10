import os
import datetime

import djcelery

"""
Django settings for cmp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# preparing Celery

djcelery.setup_loader()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*@1!+rr*%ewd#3n$426iw^q%9@1tta4e%#hji&%@n6ulyko6it'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'template'))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mptt',
    'djcelery',

    'catalog',
    'crawler',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.havuc',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'tr-TR'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# media files
# /var/www/project/static/media
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')

# media url
# /media/hede.jpg
MEDIA_URL = '/media/'

# celery configuration
BROKER_BACKEND = 'redis'
BROKER_HOST = '127.0.0.1'
BROKER_USER = ""
BROKER_PASSWORD = ""
REDIS_PORT = 6379

# Celery routing configuration
CELERY_ROUTES = {
    'crawler.tasks.crawler_job': {'queue': 'scheduled_tasks'},
    'crawler.tasks.crawle_resource': {'queue': 'crawler'},
}

CELERYBEAT_SCHEDULE = {
    'crawler_job': {
        'task': 'crawler.tasks.crawler_job',
        'schedule': datetime.timedelta(minutes=30)
    }
}

"""
Django settings for event_manager project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, locale
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o*4+4o2wia&n8_i02q9rxhhyjzzb_ueqcn=y!(ws2-z7pgydoi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',                                                                                          
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'subscribe',
    'ragazzi',
    'suit',
    'django.contrib.admin',
    'varchi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'event_manager.urls'

WSGI_APPLICATION = 'event_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'varchi': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'varchi.sqlite3'),
    },
    'bureau_prod': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'bureau.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# useful for strftime
# locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/debug.log',
        },
        'stdout' : {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'pippo': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

SUIT_CONFIG = {
    'ADMIN_NAME' : 'RN2014 - Eventi',
    'LIST_PER_PAGE' : 100,
    'SEARCH_URL' : '',
    'CONFIRM_UNSAVED_CHANGES' : False,

    'MENU' : (
        {'app': 'base', 'label': 'Gestione', },
        {'app': 'ragazzi', 'label': 'Problemi', },
        {'app': 'subscribe', 'label': 'Iscrizioni capi', },
    ),
    
}

import pika

RABBITMQ_CREDENTIAL_PASSWORD = pika.PlainCredentials('your_name', 'yourpassword')

RABBITMQ_ENABLE = False
RABBITMQ = {
    'host' : 'localhost',
    'credentials' : RABBITMQ_CREDENTIAL_PASSWORD,
}

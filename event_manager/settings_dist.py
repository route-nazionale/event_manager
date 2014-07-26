from default_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o*4+4o2wia&n8_i02q9rxhhyjzzb_ueqcn=y!(ws2-z7pgydoi'

DEBUG = True
TEMPLATE_DEBUG = True

# GOOGLE RECAPTCHA KEYS
RECAPTCHA_PUBLIC_KEY  = ''
RECAPTCHA_PRIVATE_KEY = ''

# CONTACT EMAIL FOR ERROR SUPPORT
SUPPORT_EMAIL = ''

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'event_manager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

import pika

RABBITMQ_CREDENTIAL_PASSWORD = pika.PlainCredentials('your_name', 'yourpassword')

RABBITMQ_ENABLE = False
RABBITMQ = {
    'host' : 'locahost',
    'credentials' : RABBITMQ_CREDENTIAL_PASSWORD,
}

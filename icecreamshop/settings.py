"""
Django settings for icecreamshop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$6lkna(t6j_3t57=q_*adgt49zjj-=a+5fz(3l9_^3pk)vd#w0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop',
    'ghwebhookslistener',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'icecreamshop.urls'

WSGI_APPLICATION = 'icecreamshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# Log settings (to be moved to a proper log settings file).
import logging
log = logging.getLogger('github_webhooks')
log.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)


## Continuous deployment with GitHub Webhooks #####################################################
# Setting all events to False will disable the continuous deployment.
GITHUB_WEBHOOK_EVENTS = {
    'push': True,
    'release': True,
}
GITHUB_WEBHOOK_PASSWORD = 'mypassword'
GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH = 'develop'
GITHUB_WEBHOOK_SCRIPT_TO_TRIGGER = os.path.abspath(os.path.join(BASE_DIR,
                                                                'continuous_deployment.sh'))
GITHUB_WEBHOOK_SCRIPT_LOG_FILE = os.path.abspath(os.path.join(BASE_DIR,
                                                              'continuous_deployment.log'))
###################################################################################################
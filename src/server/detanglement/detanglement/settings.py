"""
Django settings for detanglement project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Remember: Python3 compatibality: in dajaxice.core.__init__ : add . before Dajaxice import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-=*u4@e%-#%4)n8=os-53qj4ix05#o=y7)03#k)tw2q6vyn2k('
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=5
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_FRAME_DENY=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_SECURE=True
CSRF_COOKIE_AGE=2620800
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@dlocalhost'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'detanglement/templates').replace('\\', '/'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'detanglement.com', ]

ADMINS = ('Veit', 'veit.heller@hotmail.de')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'datavis',
    'djangosecure',
    'registration',
    'dajaxice',
    'dajax',
    'south'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
)

ROOT_URLCONF = 'detanglement.urls'

WSGI_APPLICATION = 'detanglement.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
CONN_MAX_AGE = 10

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tangle.db',
    }
}

# Caches
# Database Caching
# https://docs.djangoproject.com/en/dev/topics/cache/

CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'datavis',
            'TIMEOUT': 360,
            'OPTIONS': {
                'MAX_ENTRIES': 10000
            },
        }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging

OGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfile': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR+'/log.log'
                },
            },
        'loggers': {
            'dajaxice': {
                'handlers': ['logfile'],
                'level': 'DEBUG',
                'propagate': True,
                },
            }
        }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static/').replace('\\', '/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)


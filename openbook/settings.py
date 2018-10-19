"""
Django settings for openbook project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging
import logging.config
import sys

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.utils.translation import gettext_lazy  as _

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

from openbook.utils.environment import EnvironmentChecker

# Logging config
LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # root logger
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
})

logger = logging.getLogger(__name__)

# Load dotenv
load_dotenv(verbose=True, dotenv_path=find_dotenv())

# The current execution environment
ENVIRONMENT = os.environ.get('ENVIRONMENT')

if not ENVIRONMENT:
    if 'test' in sys.argv:
        logger.info('No ENVIRONMENT variable found but test detected. Setting ENVIRONMENT=TEST_VALUE')
        ENVIRONMENT = EnvironmentChecker.TEST_VALUE
    else:
        raise NameError('ENVIRONMENT environment variable is required')

environment_checker = EnvironmentChecker(environment_value=ENVIRONMENT)

# Django SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise NameError('SECRET_KEY environment variable is required')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environment_checker.is_debug()

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
if environment_checker.is_production():
    if not ALLOWED_HOSTS:
        raise NameError('ALLOWED_HOSTS environment variable is required when running on a production environment')
    ALLOWED_HOSTS = [allowed_host.strip() for allowed_host in ALLOWED_HOSTS.split(',')]
else:
    if ALLOWED_HOSTS:
        logger.info('ALLOWED_HOSTS environment variable ignored.')
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_nose',
    'openbook_auth'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'openbook.middleware.TimezoneMiddleware'
]

ROOT_URLCONF = 'openbook.urls'

AUTH_USER_MODEL = 'openbook_auth.User'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

if environment_checker.is_build():
    NOSE_ARGS = [
        '--cover-erase',
        '--cover-package=.',
        '--with-spec', '--spec-color',
        '--with-coverage', '--cover-xml',
        '--verbosity=1', '--nologcapture']
else:
    NOSE_ARGS = [
        '--cover-erase',
        '--cover-package=.',
        '--with-spec', '--spec-color',
        '--with-coverage', '--cover-html',
        '--cover-html-dir=reports/cover', '--verbosity=1', '--nologcapture']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'openbook.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# REST Framework config

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# The sentry DSN for error reporting
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if environment_checker.is_production():
    if not SENTRY_DSN:
        raise NameError('SENTRY_DSN environment variable is required when running on a production environment')
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )
else:
    if SENTRY_DSN:
        logger.info('SENTRY_DSN environment variable ignored.')

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
]

LANGUAGE_CODE = 'en'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', './files')

MEDIA_URL = os.environ.get('MEDIA_ROOT', '/files/')

"""
Django settings for sentitweet project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from pathlib import Path

import nltk
import pandas as pd
from dotenv import load_dotenv

nltk.download('stopwords') #FIXME to deltete

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps')) #for quick searching 

#Environment
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
load_dotenv()
SECRET_KEY = str(os.environ['DJANGO_SECRET_KEY'])

# DEBUG is set to False iif is False in .env otherwise it will fall back to True
DEBUG = str(os.environ.get('DEBUG')) != 'False'
if not DEBUG:
    ALLOWED_HOSTS = str(os.environ.get('ALLOWED_HOSTS')).split(',')

INSTALLED_APPS = [
    'stock',
    'tweet',
    'home',
    'authentication',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_crontab',
    'rest_framework',

    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sentitweet.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(BASE_DIR, "sentitweet/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sentitweet.context_processors.cfg_assets_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'sentitweet.wsgi.application'

# Database
DATABASE_ENV = str(os.environ.get('DATABASE_ENV'))

if DATABASE_ENV == 'production':
    database_name = os.environ.get('DATABASE_NAME')
    database_user = os.environ.get('DATABASE_USERNAME')
    database_password = os.environ.get('DATABASE_PASSWORD')
    database_host = os.environ.get('DATABASE_HOST')
    database_port = int(str(os.environ.get('DATABASE_PORT')))
else:
    database_name = 'dbsentitweet'
    database_user = 'sentitweet'
    database_password = '12345'
    database_host = 'postgres-db-sentitweet'
    database_port = 5432

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': database_name,
        'USER': database_user,
        'PASSWORD': database_password,
        'HOST': database_host,
        'PORT': database_port,
    }
}
SQLALCHEMY_DATABASE_URL = f'postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = "authentication.Contributor" 
    
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
# TODO django-allauth


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'sentitweet/static'),
) 

PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_bootstrap_components',
    'dash_renderer',
    'dpd_components',
    # 'dpd_static_support',
]
# Staticfiles finders for locating dash app assets and related files (Dash static files)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

# CRONJOBS
CRONJOBS = [
    # Everyday 15 minutes we fetch new tweets from twitter for every company
    #('*/15 * * * *', 'sentitweet.cron.fetch_new_tweets'),
    #('*/15 * * * *', 'sentitweet.cron.tweet_score_sentiment'),
]

#Dash Plotly
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Redis
# REDIS_ENV = str(os.environ.get('REDIS_ENV'))
# if REDIS_ENV == 'production':
#     redis_host = os.environ.get('REDIS_HOST')
#     redis_port = int(os.environ.get('REDIS_PORT'))
# else:
#     redis_host = '127.0.0.1'
#     redis_port = 6379

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [(redis_host, redis_port),],
#         },
#     },
# }
ASGI_APPLICATION = 'sentitweet.routing.application'

SENTITWEETAPI_SENTIMENT_X_FUNCTIONS_KEY=os.environ['SENTITWEETAPI_SENTIMENT_X_FUNCTIONS_KEY']

SENTIMENT_COMPOUND_TRHESHOLD = 0.2
DAYS_TILL_TWEETS_ARE_OUTDATED = 7

pd.options.plotting.backend = "plotly"

# Static and Media files
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'productionstaticfiles')
STATIC_URL = '/static/'

# Azure
# https://django-storages.readthedocs.io/en/latest/backends/azure.html
if os.environ.get('USE_AZURE_STATIC') == 'True':
    AZURE_ACCOUNT_NAME=os.environ.get('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY=os.environ.get('AZURE_ACCOUNT_KEY')
    AZURE_CONTAINER=os.environ.get('AZURE_CONTAINER')
    AZURE_SSL=False

    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    STATICFILES_STORAGE = 'sentitweet.storage_backends.PublicAzureStorage'
    STATIC_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/'

ASSETS_ROOT  = f'{STATIC_URL}assets'
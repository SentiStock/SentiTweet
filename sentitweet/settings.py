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
from dotenv import load_dotenv

nltk.download('stopwords')

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
    user = os.environ.get('DATABASE_USERNAME')
    password = os.environ.get('DATABASE_PASSWORD')
    host = os.environ.get('DATABASE_HOST')
    port = int(str(os.environ.get('DATABASE_PORT')))
else:
    database_name = 'dbsentitweet'
    user = 'sentitweet'
    password = '12345'
    host = 'postgres-db-sentitweet'
    port = 5432

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': database_name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
}
SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database_name}'

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

# Static and Media files
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ASSETS_ROOT = '/static/assets'

STATIC_ROOT = os.path.join(BASE_DIR, 'productionstaticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'sentitweet/static'),
) 

# CRONJOBS
CRONJOBS = [
    # Everyday at 02:00 we fetch new tweets from twitter for every company
    ('*/15 * * * *', 'sentitweet.cron.fetch_new_tweets'),
]

SENTITWEETAPI_SENTIMENT_X_FUNCTIONS_KEY=os.environ['SENTITWEETAPI_SENTIMENT_X_FUNCTIONS_KEY']
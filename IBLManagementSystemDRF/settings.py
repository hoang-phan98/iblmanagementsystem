"""
Django settings for IBLManagementSystemDRF project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Detect whether running on Lambda
IS_LAMBDA = bool(os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
ZAPPA_STAGE = os.environ.get('STAGE')
ZAPPA_PROJECT = os.environ.get('PROJECT')

if IS_LAMBDA and (not ZAPPA_STAGE or not ZAPPA_PROJECT):
    raise RuntimeError(
        "Zappa STAGE and PROJECT env variables must be defined when running in a Lambda")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=^#@o-cy6#x&rcg5##5s(gexy_@8-uw!%_8s%_@gln00qjtx$)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1",
                 ".execute-api.ap-southeast-2.amazonaws.com"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'IBLManagementSystemDRF',
    'core',
    'corsheaders',
    'django_s3_sqlite',
    'drf_yasg',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'IBLManagementSystemDRF.urls'

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

WSGI_APPLICATION = 'IBLManagementSystemDRF.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# SQLite config, TODO: Postgres config
# Override old sqlite3 on Lambda
if IS_LAMBDA:
    import sys
    sys.modules['sqlite3'] = __import__('pysqlite3')
    DATABASES = {
        'default': {
            "ENGINE": 'django_s3_sqlite',
            "NAME": f'{ZAPPA_PROJECT}-{ZAPPA_STAGE}.db',
            "BUCKET": 'fit3170-ibl-lambda-db',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ibl-dev',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = f'/{ZAPPA_STAGE}/static/' if ZAPPA_STAGE else '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_STATIC_PREFIX = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Swagger
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# CORS configurations for deployed websites
CORS_ORIGIN_WHITELIST = [
    "https://d3jlac0jbsd1oq.cloudfront.net",
    "http://fit3170-ibl-2020-dev.s3-website-ap-southeast-2.amazonaws.com"
]

# Allow localhost CORS requests
CORS_ORIGIN_REGEX_WHITELIST = [
    r"http://localhost:\d+$",
    r"http://127\.0\.0\.1:\d+$"
]

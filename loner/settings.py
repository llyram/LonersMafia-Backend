"""
Django settings for loner project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import environ
from pathlib import Path
from email.headerregistry import Address
from logging.handlers import SysLogHandler


env = environ.Env()
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# TODO: SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value('SECRET_KEY', default='django-insecure-)scsh6_myslqst35cyvnv2@^0a-z7^zaw=r#b7*tai2z5%ypzz')

# TODO: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

USESQLITE_DEV=False # to use sqlite database set this to true in development, to use sqlite

ALLOWED_HOSTS = []

if DEBUG:
    ALLOWED_HOSTS = ['localhost', 'localhost:8000', 'localhost:3000', env.get_value('DEV_ALLOWED_IP')]

else:
    ALLOWED_HOSTS = env('ALLOWED_PROD_HOSTS').replace(' ', '').split(',')

CORS_ALLOWED_ORIGINS = []

CORS_ORIGIN_WHITELIST = []

if DEBUG:
    CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://localhost', 'http://localhost:8000', 
                            'http://127.0.0.1:3000', env.get_value('DEV_ALLOWED_CORS')]
    CORS_ORIGIN_WHITELIST = ['http://localhost:3000', env.get_value('DEV_ALLOWED_CORS')]
    # CORS_ORIGIN_ALLOW_ALL=True
    CORS_ALLOW_CREDENTIALS = True
    CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', env.get_value('DEV_ALLOWED_CORS')]


SITE_DOMAIN = 'https://lonersmafia.com'

if DEBUG:
    SITE_DOMAIN = 'http://localhost:8000'


MEDIA_DOMAIN = '' # you can use subdomins to server media files

if DEBUG:
    MEDIA_DOMAIN = 'http://localhost:8000'

# else:
#     MEDIA_DOMAIN = env.get_value('AWS_S3_CUSTOM_DOMAIN') # this isn't required in production

# Application definition
INSTALLED_APPS = [

    #3rd party
    'corsheaders',
    'channels',
    'rest_framework',

    'storages', # for aws

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'user',
    'mafia',
]

AUTH_USER_MODEL = "user.User" 

if DEBUG:
    channels_hosts = [('127.0.0.1', '6379')]

else:
    channels_hosts = [(env('CHANNEL_LAYER_HOST'), env('CHANNEL_LAYER_PORT'))]


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": channels_hosts,
        },
    },
}


MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loner.urls'


DEFAULT_RENDERER_CLASSES = ( # don't provide browsable API in production
    'rest_framework.renderers.JSONRenderer', 
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.CustomPageNumber',
    'PAGE_SIZE': 7 if DEBUG else 20,
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '100/min'
    },

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                # BASE_DIR.joinpath('static'),
                BASE_DIR.joinpath('build'),
                BASE_DIR.joinpath('templates', 'admin-login'),
        ],
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

# WSGI_APPLICATION = 'loner.wsgi.application'
ASGI_APPLICATION = 'loner.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if DEBUG:
    if USESQLITE_DEV:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }

    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': env('DEV_DB_NAME'),
                'USER': env('DEV_DB_USER'),
                'PASSWORD': env('DEV_DB_PASSWORD'),
                'HOST': env('DEV_DB_HOST'),
                'PORT': '5432',
            }
        }

else:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': env('PROD_DB_NAME'),
                'USER': env('PROD_DB_USER'),
                'PASSWORD': env('PROD_DB_PASSWORD'),
                'HOST': env('PROD_DB_HOST'),
                'PORT': env('PROD_DB_PORT'),
            }
        }


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # This is only for development

else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # for production


# DEFAULT_FROM_EMAIL = Address(display_name="loners mafia", addr_spec=EMAIL_HOST_USER)



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


if not DEBUG:
    AWS_ACCESS_KEY_ID = env.get_value('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env.get_value('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env.get_value('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_REGION_NAME = env.get_value('AWS_S3_REGION_NAME')
    AWS_QUERYSTRING_AUTH = bool(int(env.get_value('AWS_QUERYSTRING_AUTH'))) # True/False value
    AWS_S3_CUSTOM_DOMAIN = env.get_value('AWS_S3_CUSTOM_DOMAIN')  
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': f'max-age={env.get_value("AWS_CACHE_MAX_AGE")}'}
    AWS_DEFAULT_ACL = None

    # AWS_LOCATION = env.get_value('AWS_LOCATION')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('static')

STATICFILES_DIRS = [
    BASE_DIR.joinpath('templates'),
    BASE_DIR.joinpath('build'),
    # BASE_DIR.joinpath('build', 'static'),
]



if DEBUG:
    MEDIA_URL ='/media/'
    MEDIA_ROOT = BASE_DIR.joinpath('media')

else:
    DEFAULT_FILE_STORAGE = 'loner.s3storage.MediaStore'
    MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# enables logging in production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        # Send info messages to syslog
        'syslog':{
            'level':'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'address': '/dev/log',
            'formatter': 'verbose',
        },
        # Warning messages are sent to admin emails
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # critical errors are logged to sentry
        # 'sentry': {
        #     'level': 'ERROR',
        #     'filters': ['require_debug_false'],
        #     'class': 'raven.contrib.django.handlers.SentryHandler',
        # },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
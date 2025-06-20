"""
Django settings for Ronix project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'users.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#ls+u)9u%%jgu9q989ke1t)mrmc$ro5cq-r@*bqg)38wpt&!%7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", '139.59.62.159']


# Application definition


AUTHENTICATION_BACKENDS = [
    'users.authentication.PasswordOrCodeBackend',
    'django.contrib.auth.backends.ModelBackend',
]


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parler',
    'contact',
    'products',
    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
    'drf_yasg',
    'users',
    'locations',
    'pages',
    'order',
    'core',
    'home',
    'parler_rest',
    'stats',
    'cart',
    'payment',
]


PAYME = {
    "PAYME_ID": config("PAYME_ID"),
    "PAYME_ACCOUNT": config("PAYME_ACCOUNT"),
    "PAYME_CALL_BACK_URL": config("PAYME_CALL_BACK_URL"),
    "PAYME_URL": config("PAYME_URL"),
}

CLICK = {
    "MERCHANT_ID": config("CLICK_MERCHANT_ID",),
    'MERCHANT_USER_ID': config("CLICK_MERCHANT_USER_ID",),
    "SERVICE_ID": config("CLICK_SERVICE_ID"),
    "SECRET_KEY": config("CLICK_SECRET_KEY"),
    "RETURN_URL": config("CLICK_RETURN_URL"),
    "PAYMENT_URL": config("CLICK_PAYMENT_URL")
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     # "https://yourfrontend.com",
# ]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'Ronix.urls'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis-test:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
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

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT format: Bearer <your_token>'
        }
    }
}

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
ADMIN_EMAIL = config('ADMIN_EMAIL')

GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI")

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

WSGI_APPLICATION = 'Ronix.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE","django.db.backends.postgresql"),
        'NAME': os.environ.get("SQL_DATABASE","ronix_db"),
        'USER': os.environ.get("SQL_USER","ronix_user"),
        'PASSWORD': os.environ.get("SQL_PASSWORD","ronix_pass"),
        'HOST': os.environ.get("SQL_HOST","db_ronix"),
        'PORT': os.environ.get("SQL_PORT","5432"),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/


LANGUAGE_CODE = 'en'
LANGUAGE_COOKIE_NAME = "lang"

LANGUAGES = (
    ('en', 'English'),
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'uz'},
        {'code': 'ru'},
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Tashkent'

JAZZMIN_SETTINGS = {
    'language_chooser': True,
    'site_brand': "Ronix site",
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static_root/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


MEDIA_URL = 'media/'
MEDIA_ROOT = 'media/'



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


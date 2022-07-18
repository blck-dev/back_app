"""
Django settings for test_backend project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import datetime
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_PATH = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env_file = os.path.join(PROJECT_PATH, "environment/.env.local")

if os.path.exists(env_file):
    print("we got env working!!")
    env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["*"]
)

ACTIVE_SEPS = ["sep-1", "sep-6", "sep-10", "sep-12", "sep-24", "sep-31"]
# Application definition

INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd apps
    'rest_framework',
    'rest_framework_swagger',
    'drf_yasg',
    "djoser",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    "polaris",

    # my apps
    'tontine',
    'accounts',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'polaris.middleware.TimezoneMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

ROOT_URLCONF = 'test_backend.urls'

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

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]

WSGI_APPLICATION = 'test_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
print("environ ----- ", os.environ.get("SQL_HOST", "localhost"))
DATABASES = {
    # 'default': env.db(
    #    "DEFAULT_URL", default="sqlite:////" + os.path.join(BASE_DIR, "data/db.sqlite3")
    # )
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", "backend_test"),
        "USER": os.environ.get("SQL_USER", "abdoufermat5@blckdev.sn"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "Fanta1976"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True
CORS_ORIGIN_ALLOW_ALL = True
APPEND_SLASH = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

VENV_PATH = os.path.dirname(BASE_DIR)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST FRAMEWORK
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
    "PAGE_SIZE": 10,

}

# Email settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default=None)
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# CORS configuration


REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('JWT', 'Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

AUTHENTICATION_BACKENDS = (

    # Important for accessing admin with django_social
    # 'social_core.backends.google.GoogleOAuth2',
    'test_backend.oauth.google.CustomGoogleOAuth2',  # Optional in case
    'django.contrib.auth.backends.ModelBackend',
)

# social_django (social-auth-app-django)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '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'  # obtained from google developers console
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # obtained from google developers console

# Fields that get saved in JSON string along with the token
# To see the data add social_django to installed apps in order
# to access this in /admin/ site
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['picture', 'locale', 'uuid']

white_list = [
    'http://localhost:8000/accounts/profile/']  # has to be the same as redirect URL on google developers console for Google OAuth2

DJOSER = {
    "LOGIN_FIELD": "email",
    'SERIALIZERS': {
        'user': 'test_backend.djoser.serializers.CustomUserSerializer',
        'current_user': 'test_backend.djoser.serializers.CustomUserSerializer',
    },
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': white_list  # Essential for obtaining redirect_uri
}

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{asctime} - {levelname} - {message}", "style": "{", },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "loggers": {
        'test_backend': {
            'handlers': ['console'],
            'propogate': True,
            'LEVEL': 'DEBUG'
        },
        "django": {
            "handlers": ["console"],
            "propogate": False,
            "level": "INFO"
        },
        "polaris": {
            "handlers": ["console"],
            "propogate": False,
            "level": "DEBUG"
        },
    },
}

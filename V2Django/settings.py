"""
Django settings for V2Django project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from typing import Tuple

import environ
from yarl import URL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")
env.prefix = "DJANGO__"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "V2Django",
    "Users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

ROOT_URLCONF = "V2Django.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "V2Django.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": env.db_url(
        "DATABASE_DSN", default=f"sqlite:///{BASE_DIR}/storage/sqlite.db"
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = env.path("STATIC_ROOT", default=BASE_DIR / "statics")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# app
V2USER_URI = URL(env.str("V2USER_URI"))
INFLUX_URI = URL(env.str("INFLUX_URI"))
INFLUX_BUCKET_USER_STATS = env.str("INFLUX_BUCKET_USER_STATS")

USER_DEFAULT_SUBS_DURATION = env.str("USER_DEFAULT_SUBS_DURATION", 30)
USER_DEFAULT_SUBS_VOLUME = env.str("USER_DEFAULT_SUBS_VOLUME", "10Gb")
USER_INIT_ON_START = env.bool("USER_INIT_ON_START", default=True)

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_INTERVAL_V2RAYPROFILE_UPDATE = env.int(
    "CELERY_INTERVAL_V2RAYPROFILE_UPDATE", 60
)
CELERY_BEAT_SCHEDULE = {
    "task__v2rayprofile_update": {
        "task": "Users.tasks.task__v2rayprofile_update",
        "schedule": CELERY_INTERVAL_V2RAYPROFILE_UPDATE,
    }
}

WH_USER_EXPIRE = URL(env.str("WH_USER_EXPIRE", ""))
WH_SUBSCRIPTION_EXPIRE = URL(env.str("WH_SUBSCRIPTION_EXPIRE", ""))
WH_USER_ACTIVATE = URL(env.str("WH_USER_ACTIVATE", ""))
WH_SUBSCRIPTION_ACTIVATE = URL(env.str("WH_SUBSCRIPTION_ACTIVATE", ""))

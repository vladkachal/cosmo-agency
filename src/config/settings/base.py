"""
This file contains the base settings for a project. It provides a foundational
configuration for building other settings files (e.g., development, production).

To use this file, create a new settings file and import this one as the base.
Then, you can override any of the settings in this file or add a new settings
as needed for a project.
"""

from pathlib import Path

from decouple import Csv, config

CURRENT_ENVIRONMENT = config("CURRENT_ENVIRONMENT")


class CurrentEnv:
    is_dev = CURRENT_ENVIRONMENT == "development"
    is_prod = CURRENT_ENVIRONMENT == "production"
    is_stage = CURRENT_ENVIRONMENT == "staging"
    is_test = CURRENT_ENVIRONMENT == "testing"


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------------------------------------------------------------
# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
admins_csv = Csv(cast=lambda s: tuple(s.split(",")), delimiter=";")
ADMINS = config("ADMINS", cast=admins_csv, default=None)
SITE_ID = 1
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # --------------------------------------------------------------------------
    # Third-party apps
    "adminsortable2",
    "easy_thumbnails",
    "filer",
    # --------------------------------------------------------------------------
    # Local apps
    "apps.core",
    "apps.slider",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# ------------------------------------------------------------------------------
# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = config("ROOT_URLCONF", default="config.urls")
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------------------
# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "TEST": {
            "NAME": f"{config('DATABASE_NAME')}_test",
        },
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# STATIC
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ------------------------------------------------------------------------------
# MEDIA
# ------------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
USE_TZ = True
TIME_ZONE = "UTC"
USE_I18N = False

# ------------------------------------------------------------------------------
# COMPONENTS
# ------------------------------------------------------------------------------
from .components.logging_ import *  # noqa

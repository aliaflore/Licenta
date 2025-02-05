from pathlib import Path
import os

from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "licenta",
    "django_celery_beat",
    "django_celery_results",
    "dj_rest_auth",
    "drf_spectacular",
    "encrypted_model_fields",
    "djstripe",
    'corsheaders',
]

SITE_ID = 1

import corsheaders

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]

CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_REDIS_URL", default="redis://localhost:6379"
)

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 30,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Licenta API',
    'DESCRIPTION': 'Licenta',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    # OTHER SETTINGS
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "licenta.User"

CELERY_RESULT_BACKEND = "django-db"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"


TESSERACT_LANGUAGES = "eng+ron"

ANALYSIS_TRANSLATE_LANGUAGES = ["en", "ro"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": '[%(asctime)s] \033[93m%(levelname)s @ %(filename)s#%(lineno)d "%(message)s"\033[0m',
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "()": "backend.loggers.ExtraContextFormatter",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        }
    },
}

X_FRAME_OPTIONS = "SAMEORIGIN"

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

REST_AUTH = {
    'PASSWORD_RESET_SERIALIZER': 'licenta.serializers.PasswordResetSerializer'
}

STRIPE_LIVE_MODE = False
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_SUBSCRIBER_CUSTOMER_KEY = "id"

STRIPE_SUBSCRIPTION_PRICE_ID = "price_1Qo0TLRuwtXrhTLiAV3y5zlO"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
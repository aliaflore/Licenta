from pathlib import Path
import os

from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-yq8em$ly3u&z^&=o=#v6_@a^(*4()tlo-9(9#n%59bqz@o=5hs"

DEBUG = os.environ.get("DEBUG", True)

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

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
    "djstripe"
]

SITE_ID = 1

MIDDLEWARE = [
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

CELERY_TASK_ALWAYS_EAGER = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
]

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Licenta Tuc <licentatuc@tedyst.ro>"

OPENAPI_ORGANIZATION = os.getenv("OPENAPI_ORGANIZATION")
OPENAPI_PROJECT = os.getenv("OPENAPI_PROJECT")
OPENAPI_KEY = os.getenv("OPENAPI_KEY")

OPENAPI_CLIENT = OpenAI(
    organization=OPENAPI_ORGANIZATION, project=OPENAPI_PROJECT, api_key=OPENAPI_KEY
)

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

FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY', '')

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')


MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

REST_AUTH = {
    'PASSWORD_RESET_SERIALIZER': 'licenta.serializers.PasswordResetSerializer'
}

STRIPE_LIVE_MODE = False
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY")
DJSTRIPE_SUBSCRIBER_CUSTOMER_KEY = "id"

STRIPE_SUBSCRIPTION_PRICE_ID = "price_1Qo0TLRuwtXrhTLiAV3y5zlO"
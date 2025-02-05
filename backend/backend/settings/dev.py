from .common import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG = True
SECRET_KEY = "django-insecure-yq8em$ly3u&z^&=o=#v6_@a^(*4()tlo-9(9#n%59bqz@o=5hs"
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_TASK_ALWAYS_EAGER = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

OPENAPI_ORGANIZATION = os.getenv("OPENAPI_ORGANIZATION", "")
OPENAPI_PROJECT = os.getenv("OPENAPI_PROJECT", "")
OPENAPI_KEY = os.getenv("OPENAPI_KEY", "")

OPENAPI_CLIENT = OpenAI(
    organization=OPENAPI_ORGANIZATION, project=OPENAPI_PROJECT, api_key=OPENAPI_KEY
)

FIELD_ENCRYPTION_KEY = "MXtqhgTCtCt-gLgBAmNebQrrlvqr0OC4CnrhY84yLDM="

FRONTEND_URL = "http://localhost:5173"

STRIPE_TEST_SECRET_KEY = os.getenv("STRIPE_TEST_SECRET_KEY", "")
STRIPE_TEST_PUBLIC_KEY = os.getenv("STRIPE_TEST_PUBLIC_KEY", "")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:5173',
]

CORS_ALLOW_CREDENTIALS = True
from .common import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_REDIS_URL", default="redis://localhost:6379"
)
CELERY_TASK_ALWAYS_EAGER = False
CSRF_TRUSTED_ORIGINS = [
    os.getenv("FRONTEND_URL"),
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

FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY')
FRONTEND_URL = os.environ.get('FRONTEND_URL')

STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="*").split(",")

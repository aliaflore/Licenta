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
    "CELERY_BROKER_URL", default="redis://localhost:6379"
)
CELERY_TASK_ALWAYS_EAGER = False
CSRF_TRUSTED_ORIGINS = [
    "http://" + os.getenv("FRONTEND_URL", ""),
    "http://" + os.getenv("FRONTEND_URL", "").split(":")[0],
    "https://" + os.getenv("FRONTEND_URL", ""),
    "https://" + os.getenv("FRONTEND_URL", "").split(":")[0],
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
FRONTEND_URL = "http://" + os.environ.get('FRONTEND_URL', "")

STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="*").split(",")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379"),
    }
}

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "licenta-unidata"
AWS_S3_REGION_NAME = "eu-north-1"
MINIO_ENDPOINT_URL = os.environ.get("MINIO_ENDPOINT_URL")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "endpoint_url": MINIO_ENDPOINT_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
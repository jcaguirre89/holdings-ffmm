import os

from backend.settings.common import *


DATABASES = {
    "default": dj_database_url.parse(config("DATABASE_URL"), conn_max_age=600)
}

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "production")
print(ENVIRONMENT)

DEBUG = False
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


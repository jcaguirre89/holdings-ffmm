"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from decouple import config

environment = config("DJANGO_ENVIRONMENT", default="production")

if environment.lower() == 'development':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.prod")

application = get_wsgi_application()

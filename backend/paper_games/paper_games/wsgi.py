"""Конфигурация WSGI для проекта paper_games.

Больше информации:
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_games.settings')

application = get_wsgi_application()

"""Модуль для описания классов-посреников для запросов (middleware).
"""
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    """Класс-посредник для авторизации с помощью токена в Django Channels 2, используемый в модуле routing.py.
    """
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        scope['user'] = AnonymousUser()
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

"""Корневая конфигурация маршрутизации для Django Channels.
"""
from channels.routing import ProtocolTypeRouter, URLRouter
import virus_war.routing
from .middleware import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            virus_war.routing.websocket_urlpatterns
        )
    ),
})
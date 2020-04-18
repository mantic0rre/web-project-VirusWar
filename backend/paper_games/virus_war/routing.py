from django.urls import re_path
from virus_war.consumers import RoomConsumer, LobbyConsumer


websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_id>\w+)/$', RoomConsumer),
    re_path(r'ws/lobby', LobbyConsumer),
]

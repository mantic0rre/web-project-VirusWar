"""Регистрация моделей для админки.
"""
from django.contrib import admin
from virus_war.models import Room, StarredRooms, Message


admin.site.register(Room)
admin.site.register(StarredRooms)
admin.site.register(Message)

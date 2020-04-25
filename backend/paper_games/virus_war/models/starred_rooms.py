"""Избранные комнаты.
"""
from django.db import models
from rest_framework.exceptions import ValidationError


class StarredRooms(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'room'),)

    @staticmethod
    def raise_if_already_starred(user, room):
        already_starred = StarredRooms.objects.filter(user=user, room=room).exists()
        if already_starred:
            raise ValidationError('Комната уже является избранной')
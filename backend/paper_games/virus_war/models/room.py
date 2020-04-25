"""Игровая комната.
"""
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=30, unique=True)
    max_players = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    password = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey('auth.User', related_name='created_rooms', on_delete=models.CASCADE)
    sub_users = models.ManyToManyField('auth.User', related_name='starred_rooms', through='StarredRooms')

    def __str__(self):
        return '%s (%s)' % (self.name, self.owner)

    @staticmethod
    def filter_by_parameters(user, starred, hide_empty, hide_busy, search):
        """Фильт комнат для лобби по параметрам.

        Args:
            user: ссылка на пользователя
            starred (bool): Показать избранные комнаты.
            hide_empty (bool): Скрыть пустые комнтаны.
            hide_busy (bool): Скрыть заполненные команты.
            search (str): Текст поиска комнаты по её названию.

        Note:
             Приоритет параметров: \n
             1) search. Если аргумент определен, остальные параметры игнорируются.
             2) starred. Если аргумент определен, остальные параметры игнорируются.
             3) Учёт всех остальных параметров.

        Returns:
            Список комнат.
        """
        print(hide_empty, hide_busy, search)
        if search:
            return Room.objects.filter(name__contains=search)
        elif starred:
            return user.starred_rooms.all()
        return Room.objects.all()
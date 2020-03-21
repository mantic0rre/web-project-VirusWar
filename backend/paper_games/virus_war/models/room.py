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
        print(hide_empty, hide_busy, search)
        if search:
            return Room.objects.filter(name__contains=search)
        elif starred:
            return user.starred_rooms.all()
        return Room.objects.all()
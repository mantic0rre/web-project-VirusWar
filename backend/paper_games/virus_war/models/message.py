"""Сообщение в чате.
"""
from django.db import models
from rest_framework.exceptions import ValidationError


class Message(models.Model):
    room = models.ForeignKey('Room', related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return '%s/ %s/ %s/ %s' % (self.room.name, self.user, self.datetime, self.content)

    @staticmethod
    def get_portion(room, portion_num, portion_size):
        """Получить порцию сообщений.

        Note:
            Функция необходима для динамической подгрузки сообщений в чате комнаты.

        Args:
            room: ссылка на комнату.
            portion_num (int): Номер порции. Должен быть >= 0.
            portion_size (int): Размер порции. Должен быть > 0.

        Returns:
            Список сообщений.

        Raises:
            ValidationError:
        """
        if not (portion_size or portion_num):
            return Message.objects.filter(room=room)

        try:
            portion_size = int(portion_size)
            portion_num = int(portion_num)
            if portion_size <= 0 or portion_num < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValidationError({'Ошибка параметров запроса' : 'Введены некорректные значения',
                                   'Замечание': 'параметры portion_size и portion_num нельзя использовать отдельно',
                                   'Допустимые значения' : 'portion_size > 0, portion_num >= 0'})
        else:
            start = portion_num * portion_size
            end = start + portion_size
            return Message.objects.filter(room=room)[start:end]





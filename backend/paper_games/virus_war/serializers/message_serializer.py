from rest_framework import serializers
from virus_war.models import Message
from django.conf import settings


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    datetime = serializers.DateTimeField(format=settings.DATETIME_FORMAT, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'datetime', 'content']
        read_only_fields = ['datetime', 'room']
from rest_framework import serializers
from virus_war.models import Room
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    created_rooms = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all())
    starred_rooms = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'created_rooms', 'starred_rooms']
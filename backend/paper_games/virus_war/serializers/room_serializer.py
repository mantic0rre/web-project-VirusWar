from rest_framework import serializers
from virus_war.models import Room, StarredRooms


class RoomSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['sub_users', 'is_starred']

    def create(self, validated_data):
        room = Room.objects.create(**validated_data)
        StarredRooms.objects.create(user=room.owner, room=room)
        return room

    def get_is_starred(self, room):
        return self.context['request'].user.starred_rooms.filter(pk=room.id).exists()
from rest_framework import serializers
from virus_war.models import StarredRooms


class StarredSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = StarredRooms
        fields = '__all__'
        read_only_fields = ['datetime']
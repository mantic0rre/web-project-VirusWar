from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from virus_war.serializers import StarredSerializer
from virus_war.models import StarredRooms


class StarredCreate(generics.CreateAPIView):
    serializer_class = StarredSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        StarredRooms.raise_if_already_starred(self.request.user, serializer.validated_data['room'])
        serializer.save(user=self.request.user)


class StarredDestroy(generics.DestroyAPIView):
    queryset =  StarredRooms.objects.all()
    serializer_class = StarredSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = generics.get_object_or_404(StarredRooms, user=self.request.user, room=self.kwargs['room_id'])
        self.check_object_permissions(self.request, obj)
        return obj
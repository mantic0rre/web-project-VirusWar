from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from virus_war.permissions import IsOwnerOrReadOnly
from virus_war.serializers import RoomSerializer
from virus_war.models import Room


class RoomListCreate(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        starred = self.request.query_params.get('starred', False)
        hide_empty = self.request.query_params.get('hide_empty', False)
        hide_busy = self.request.query_params.get('hide_busy', False)
        search = self.request.query_params.get('search', None)
        return Room.filter_by_parameters(self.request.user, starred, hide_empty, hide_busy, search)


class RoomRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
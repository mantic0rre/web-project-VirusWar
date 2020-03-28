from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from virus_war.permissions import IsAuthorOrReadOnly
from virus_war.serializers import MessageSerializer
from virus_war.models import Room, Message


class MessageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room = generics.get_object_or_404(Room, pk=self.kwargs['room_id'])
        portion_size = self.request.query_params.get('portion_size')
        portion_num = self.request.query_params.get('portion_num')
        return Message.get_portion(room, portion_num, portion_size)

    def perform_create(self, serializer):
        room = generics.get_object_or_404(Room, pk=self.kwargs['room_id'])
        serializer.save(room=room, user=self.request.user)


class MessageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
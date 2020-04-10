from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from virus_war.models import Message, Room


class RoomConsumer(JsonWebsocketConsumer):
    lobby_group_name = 'lobby'

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'room_%s' % self.room_id
        self.user = self.scope["user"]

        try: self.room = Room.objects.get(pk=self.room_id)
        except Room.DoesNotExist: return

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        msg_type = content['type']
        print(content)

        if msg_type == 'auth':
            token_key = content['token']
            token = None
            try: token = Token.objects.get(key=token_key)
            except Token.DoesNotExist: return 
            self.scope['user'] = token.user
            self.user = self.scope['user']
            return

        # === Next types require authorization ===
        if isinstance(self.scope['user'], AnonymousUser):
            self.close()
            return

        if msg_type == 'chat':
            message = Message.objects.create(room=self.room, user=self.scope['user'], content=content['content'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': msg_type,
                    'user': message.user.username,
                    'content': message.content,
                    'datetime': message.datetime.strftime(settings.DATETIME_FORMAT)
                })
            return

    # === Send to all ===

    def chat(self, event):
        self.send_json(
        {
            'type': event["type"],
            'user': event["user"],
            'content': event["content"],
            'datetime': event["datetime"]
        })

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from virus_war.models import Message, Room
from virus_war.game.game_engine import *


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

        state = GameEngine.game_status(self.room.id)
        self.send_json(
            {
                'type': 'connect',
                'code': state.dict['code'],
                'board': state.dict['data']['board'],
                'ready_players': state.dict['data']['ready_players'],
            })

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        if not isinstance(self.user, AnonymousUser):
            state = self.util_remove_player()
            self.util_game_info_to_lobby(state)

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

         # === Game ===
        state = None
        if msg_type == 'readiness':
            figure = content['figure']
            state = GameEngine.readiness(self.room, self.user, figure)
            self.send_json(
            {
                'type': msg_type + '_personal',
                'code': state.dict['code'],
            })
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': msg_type,
                    'ready_players': state.dict['data']['ready_players']
                })
        elif msg_type == 'start':
            state = GameEngine.start(self.room.id)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': msg_type,
                    'code': state.dict['code'],
                    'cur_figure': state.dict['data']['cur_figure']
                })
        elif msg_type == 'take_move':
            state = GameEngine.take_move(self.room.id, content['i'], content['j'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': msg_type,
                    'code': state.dict['code'],
                    'is_implemented': state.dict['data']['is_implemented'],
                    'cell': state.dict['data']['cell'],
                    'cur_figure': state.dict['data']['cur_figure'],
                    'ready_players': state.dict['data']['ready_players'],
                    'i': content['i'],
                    'j': content['j']
                })
        elif msg_type == 'remove_player':
            state = self.util_remove_player()

        self.util_game_info_to_lobby(state)

    # === Utility ===

    def util_remove_player(self):
        state = GameEngine.remove_player(self.room.id, self.user.username)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'remove_player',
                'code': state.dict['code'],
                'ready_players': state.dict['data']['ready_players'],
                'cur_figure': state.dict['data']['cur_figure'],
            })
        return state

    def util_game_info_to_lobby(self, state):
        dirty = state.dict['data'].get('dirty')
        if dirty:
            code = state.dict['code']
            ready_players = state.dict['data']['ready_players']
            number_of_players = len(ready_players) if ready_players else 0
            async_to_sync(self.channel_layer.group_send)(
                RoomConsumer.lobby_group_name,
                {
                    'type': 'new_room_info',
                    'room_id': self.room.id,
                    'game_is_on': True if (code == GAME_IS_ON or code == GAME_START) else False,
                    'number_of_players': number_of_players
                })

    # === Send to all ===

    def chat(self, event):
        self.send_json(
        {
            'type': event["type"],
            'user': event["user"],
            'content': event["content"],
            'datetime': event["datetime"]
        })

    def readiness(self, event):
        self.send_json(
        {
            'type': event["type"],
            'ready_players': event["ready_players"],
        })

    def start(self, event):
        self.send_json(
        {
            'type': event["type"],
            'code': event["code"],
            'cur_figure': event["cur_figure"]
        })

    def take_move(self, event):
        self.send_json(
        {
            'type': event['type'],
            'code': event['code'],
            'is_implemented': event['is_implemented'],
            'cell': event['cell'],
            'cur_figure': event['cur_figure'],
            'ready_players': event['ready_players'],
            'i': event['i'],
            'j': event['j'],
        })

    def remove_player(self, event):
        self.send_json(
        {
            'type': event["type"],
            'code': event["code"],
            'ready_players': event["ready_players"],
            'cur_figure': event["cur_figure"],
        })

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from virus_war.game import GameEngine


class LobbyConsumer(JsonWebsocketConsumer):
    lobby_group_name = 'lobby'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            LobbyConsumer.lobby_group_name,
            self.channel_name
        )
        self.accept()

        self.send_json(
        {
            'type': 'games_info',
            'data': GameEngine.games_info()
        })

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            LobbyConsumer.lobby_group_name,
            self.channel_name
        )

    def new_room_info(self, event):
        self.send_json(
        {
            'type': event["type"],
            'room_id': event['room_id'],
            'game_is_on': event["game_is_on"],
            'number_of_players': event["number_of_players"],
        })



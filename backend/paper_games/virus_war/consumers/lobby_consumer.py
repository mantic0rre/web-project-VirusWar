from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from virus_war.game import GameEngine


class LobbyConsumer(JsonWebsocketConsumer):
    """Обмен сообщениями по WebSocket в лобби.

    Сообщения отправляются и принимаются в формате json. Существует одна группа пользователей, находящихся в лобби.
    """
    lobby_group_name = 'lobby'

    def connect(self):
        """Добавление пользователя в группу. Установление соединения. Отправка данных об играх.
        """
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
        """Вызывается, когда закрывается соединение.
        """
        async_to_sync(self.channel_layer.group_discard)(
            LobbyConsumer.lobby_group_name,
            self.channel_name
        )

    def new_room_info(self, event):
        """Событие. Приём и отправка каждому пользователю обновления данных об играх.
        """
        self.send_json(
        {
            'type': event["type"],
            'room_id': event['room_id'],
            'game_is_on': event["game_is_on"],
            'number_of_players': event["number_of_players"],
        })



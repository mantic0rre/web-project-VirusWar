from .virus_war import VirusWar

GAME_IS_ON = 0
GAME_IS_NOT_ON = 1
GAME_START = 2
GAME_END = 3
POS_CONFIRM = 4
POS_CANCEL = 5
POS_CHANGE = 6
POS_DENIED = 7
POS_NO_READY = 8


class State(object):
    """Состояние игры.

    Args:
        code (int): Код состояния игры.
        data (dict): Словарь, содержащий данные о текущем состоянии игры.
    """
    def __init__(self, code, data):
        state = {}
        state['code'] = code
        state['data'] = data
        self.__state = state

    @property
    def dict(self):
        return self.__state


class Engine(object):
    """Движок игры. Хранилище игр в RAM.

    Note:
        Любое действие в игре возвращает State.
    """
    def __init__(self):
        self.__running_games = dict()
        self.__ready_players = dict()

    def readiness(self, room, user, figure):
        """Подтвердить готовность играть. Занять позицию.

        Args:
            room: Ссылка на комнату.
            user: Ссылка на пользователя.
            figure (int): Номер фигуры.

        Returns:
            State: \n
            * 'code': Код состояния игры.
            * 'data': \n
                * 'ready_players' (dict): Список готовых игроков.
                * 'dirty' (bool): Флаг изменений.
        """
        RunningGames = self.__running_games
        ReadyPlayers = self.__ready_players
        username = user.username

        # game is on
        if RunningGames.get(room.id):
            return State(GAME_IS_ON, {'ready_players': None, 'dirty': False})

        # no ready players (init dict)
        if not ReadyPlayers.get(room.id):
            ReadyPlayers[room.id] = {username: figure}
            return State(POS_CONFIRM, {'ready_players': ReadyPlayers[room.id], 'dirty': True})

        # confirm position for the first time
        ready_players = ReadyPlayers[room.id]
        if not ready_players.get(username):
            if not figure in ready_players.values():
                ready_players[username] = figure
                # check for start
                if len(ready_players) == room.max_players:
                    figure_order = list(ready_players.values())
                    RunningGames[room.id] = VirusWar(room.height, room.width, figure_order)
                    return State(GAME_START, {'ready_players': ready_players, 'dirty': True})
                return State(POS_CONFIRM, {'ready_players': ready_players, 'dirty': True})
            return State(POS_DENIED, {'ready_players': ready_players, 'dirty': False})

        # cancel
        user_figure = ready_players[username]
        if user_figure == figure:
            ready_players.pop(username)
            if len(ready_players) == 0:
                ReadyPlayers.pop(room.id)
                return State(POS_NO_READY, {'ready_players': None, 'dirty': True})
            return State(POS_CANCEL, {'ready_players': ready_players, 'dirty': True})

        # change position (other figure)
        if not figure in ready_players.values():
            ready_players[username] = figure
            return State(POS_CHANGE, {'ready_players': ready_players, 'dirty': True})
        return State(POS_DENIED, {'ready_players': ready_players, 'dirty': False})

    def start(self, room_id):
        """Инициирование начала игры.

        Args:
            room_id (int): Номер комнаты.

        Returns:
            State: \n
            * 'code': Код состояния игры.
            * 'data': \n
                * 'cur_figure' (int): Номер текущей фигуры.
        """
        game = self.__running_games.get(room_id)
        if game:
            return State(GAME_IS_ON, {'cur_figure': game.cur_figure})
        return State(GAME_IS_NOT_ON, {'cur_figure': None})

    def game_status(self, room_id):
        """Получить информацию об игре.

        Args:
            room_id (int): Идентификатор комнаты.

        Returns:
            State: \n
            * 'code': Код состояния игры.
            * 'data': \n
                * 'board' (list of list): Матрица игрового поля.
                * 'ready_players' (dict): Список готовых игроков.
        """
        game = self.__running_games.get(room_id)
        ready_players = self.__ready_players.get(room_id)
        if game:
            return State(GAME_IS_ON, {'board': game.board, 'ready_players': ready_players})
        return State(GAME_IS_NOT_ON, {'board': None, 'ready_players': ready_players})

    def take_move(self, room_id, i, j):
        """Совершить ход.

        Args:
            room_id (int): Идентификатор комнаты.
            i (int): Номер строки игрового поля.
            j (int): Номер столбца игрового поля.

        Returns:
            State: \n
            * 'code': Код состояния игры.
            * 'data': \n
                * 'is_implemented' (bool): Была ли изменена матрица.
                * 'cell' (int): Значение клетки, в которую был совершен ход.
                * 'cur_figure' (int): Номер фигуры, чей ход.
                * 'ready_players' (dict): Список готовых игроков (игроков в игре).
                * 'dirty' (bool): Флаг изменений.
        """
        game = self.__running_games.get(room_id)
        players = self.__ready_players.get(room_id)
        if game:
            move_data = game.take_move(i, j)
            is_implemented = move_data['is_implemented']
            cell = move_data['cell']
            game_over = move_data['game_over']
            cur_figure = move_data['cur_figure']
            blocked = move_data['blocked']

            if game_over:
                self.__ready_players.pop(room_id)
                self.__running_games.pop(room_id)
                return State(GAME_END, {'is_implemented': is_implemented, 'cell': cell, 'cur_figure': cur_figure, 'ready_players': None, 'dirty': True})

            names_block = []
            for username in players.keys():
                if players[username] in blocked:
                    names_block.append(username)

            for name in names_block:
                players.pop(name)

            return State(GAME_IS_ON, {'is_implemented': is_implemented, 'cell': cell, 'cur_figure': cur_figure, 'ready_players': players, 'dirty': len(blocked) != 0})
        return State(GAME_IS_NOT_ON, {'is_implemented': None, 'cell': None, 'cur_figure': None, 'ready_players': None, 'dirty': None})

    def remove_player(self, room_id, username):
        """Удалить игрока.

        Args:
            room_id (int): Идентификатор комнаты.
            username (str): Уникальное имя пользователя.

        Returns:
            State: \n
            * 'code': Код состояния игры.
            * 'data': \n
                * 'ready_players' (dict): Список готовых игроков (игроков в игре).
                * 'cur_figure' (int): Номер фигуры, чей ход.
                * 'dirty' (bool): Флаг изменений.
        """
        game = self.__running_games.get(room_id)
        players = self.__ready_players.get(room_id)
        if players:
            figure = players.get(username)
            if figure:
                players.pop(username)
        if game:
            remove_data = game.remove_figure(figure)
            game_over, cur_figure = remove_data['game_over'], remove_data['cur_figure']
            if game_over:
                self.__ready_players.pop(room_id)
                self.__running_games.pop(room_id)
                return State(GAME_END, {'ready_players': None, 'cur_figure': cur_figure, 'dirty': True})
            return State(GAME_IS_ON, {'ready_players': players, 'cur_figure': cur_figure, 'dirty': True})
        return State(GAME_IS_NOT_ON, {'ready_players': players, 'cur_figure': None, 'dirty': None})

    def games_info(self):
        """Получить информацию об играх.

        Returns:
            dict: \n
            * key (int): Идентификатор комнаты.
            * value (dict): \n
                * 'number_of_players' (int): Количество готовых игроков.
                * 'game_is_on' (bool): Флаг идущей игры.
        """
        ready_players = self.__ready_players
        ret = {}
        for room_id in ready_players:
            number_of_players = len(ready_players[room_id])
            game_is_on = True if self.__running_games.get(room_id) else False
            ret[room_id] = { "number_of_players": number_of_players, "game_is_on": game_is_on}
        return ret


print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~ Init GameEngine! ~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
GameEngine = Engine()

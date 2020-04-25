from collections import deque
from copy import deepcopy


class VirusWar(object):
    """Игра 'Война Вирусов' на одном игровом поле.

    Args:
        h (int): Высота игрового поля. Количество клеток в высоту.
        w (int): Ширина игрового поля. Количество клеток в ширину.
        figure_order (list of int): Список с номерами фигур. Порядок фигур определяет последовательсноть ходов.

    Note:
        Нумерация фигур на игровом поле для 4 игроков соответсвтует написанию буквы z через углы прямоуольного поля.

    Note:
        Класс хранит состояние игры в виде целочисленной матрицы. Соглашение о заполнении матрицы: \n
        * 0 - путая клетка;
        * 1-9 - номер фигуры (игрока);
        * 10-99 - перекрытие фигур: вторая цифра обозначает фигуру, которая перекрывает первую.

    Todo:
        * Текущая реализация предполагает до 4 игроков на прямоугольном поле.
        * Можно увеличить максимальное количество игроков.
    """
    def __init__(self, h, w, figure_order):
        self._h, self._w  = h, w
        self._board = [[0 for col in range(w)] for row in range(h)]
        self._figure_order = figure_order

        for figure in figure_order:
            if figure == 1: self._board[0][0] = figure
            elif figure == 2: self._board[0][w-1] = figure
            elif figure == 3: self._board[h-1][0] = figure
            elif figure == 4: self._board[h-1][w-1] = figure

        self._cur_index = 0
        self._cur_figure = figure_order[0]
        self._cur_stamina = 3

    @property
    def board(self):
        """list of list: Матрица игрового поля."""
        return self._board

    @property
    def cur_figure(self):
        """int: Номер текущей фигуры."""
        return self._cur_figure

    def take_move(self, i, j):
        """Совершить ход.

        Args:
            i (int): Номер строки.
            j (int): Номер столбца.

        Returns:
            dict: \n
            * 'is_implemented' (bool): Была ли изменена матрица.
            * 'cell' (int): Значение клетки, в которую был совершен ход.
            * 'game_over' (bool): Флаг окончания игры.
            * 'cur_figure' (int): Номер фигуры, чей ход.
            * 'blocked' (list of int): Список с номерами фигур (игроков), которые полностью заблокированы и выходят из игры.
        """
        if self.__enable_to_infect(i, j):
            self.__infect(i, j)
            if not self.__use_and_check_stamina():
                self.__switch_figure()
            data = self.__remove_blocked()
            return {'is_implemented': True, 'cell': self._board[i][j], 'game_over': data['game_over'], 'cur_figure': data['cur_figure'], 'blocked': data['blocked']}
        return {'is_implemented': False, 'cell': self._board[i][j], 'game_over': False, 'cur_figure': self.cur_figure, 'blocked': []}

    def enable_to_move(self):
        """Проверка возможности совершить ход."""
        for i in range(self._h):
            for j in range(self._w):
                if self.__enable_to_infect(i, j):
                    return True
        return False

    def remove_figure(self, figure):
        """Удаление игрока.

        Args:
            figure (int): Номер удаляемой фигуры (игрока).

        Returns:
            dict: \n
            * 'game_over' (bool): Флаг окончания игры.
            * 'cur_figure' (int): Номер фигуры, чей ход.
        """
        assert (figure in self._figure_order)
        index_remove = self._figure_order.index(figure)
        self._figure_order.remove(figure)
        if len(self._figure_order) == 1:
            self._cur_index = 0
            self._cur_figure = -1
            return {'game_over': True, 'cur_figure': self._figure_order[0]}

        if index_remove >= self._cur_index:
            self._cur_index = self._cur_index % len(self._figure_order)
        else:
            self._cur_index -= 1
        self._cur_figure = self._figure_order[self._cur_index]
        return {'game_over': False, 'cur_figure': self._cur_figure}

    # === Utility ===

    def __remove_blocked(self):
        blocked = self.__get_blocked_figures()
        if len(blocked) == 0:
            return {'game_over': False, 'cur_figure': self.cur_figure, 'blocked': blocked}

        if len(blocked) == len(self._figure_order):
            return {'game_over': True, 'cur_figure': None, 'blocked': blocked}

        remove_data = None
        for figure in blocked:
            remove_data = self.remove_figure(figure)
        remove_data['blocked'] = blocked
        return remove_data

    def __get_blocked_figures(self):
        keep_index = self._cur_index
        keep_figure = self._cur_figure
        blocked = []
        for figure in self._figure_order:
            self._cur_figure = figure
            if not self.enable_to_move():
                blocked.append(figure)
        self._cur_index = keep_index
        self._cur_figure = keep_figure
        return blocked

    def __switch_figure(self):
        self._cur_index += 1
        self._cur_index = self._cur_index % len(self._figure_order)
        self._cur_figure =  self._figure_order[self._cur_index]
        return self._cur_figure

    def __use_and_check_stamina(self):
        self._cur_stamina -= 1
        if not self._cur_stamina:
            self._cur_stamina = 3
            return False
        return True

    def __enable_to_infect(self, i, j):
        cell = self._board[i][j]
        return cell != self._cur_figure and (0 <= cell < 10) and self.__connected_chain_is_nearby(i, j)

    def __infect(self, i, j):
        cell = self._board[i][j]
        infection = self._cur_figure
        if cell > 0:
            infection = cell * 10 + self._cur_figure
        self._board[i][j] = infection
        return infection

    def __connected_chain_is_nearby(self, i, j):
        board = deepcopy(self._board)
        stack = deque()
        stack.append((i, j))
        while len(stack) != 0:
            coord = stack.pop()
            i, j = coord[0], coord[1]
            for pair in self.__get_neighboring_cells(i, j):
                neighbor = board[pair[0]][pair[1]]
                if neighbor == self._cur_figure:
                    return True
                if neighbor % 10 == self._cur_figure:
                    board[pair[0]][pair[1]] = 0
                    stack.append(pair)
        return False

    def __get_neighboring_cells(self, i, j):
        h, w = self._h, self._w
        east_is_available = j + 1 < w
        north_is_available = i - 1 >= 0
        west_is_available = j - 1 >= 0
        south_is_available = i + 1 < h

        east = (i, j + 1)
        northeast = (i - 1, j + 1)
        north = (i - 1, j)
        northwest = (i - 1, j - 1)
        west = (i, j - 1)
        southwest = (i + 1, j - 1)
        south = (i + 1, j)
        southeast = (i + 1, j + 1)

        if not east_is_available:
            east, northeast, southeast = None, None, None
        if not north_is_available:
            north, northwest, northeast = None, None, None
        if not west_is_available:
            west, northwest, southwest = None, None, None
        if not south_is_available:
            south, southwest, southeast = None, None, None

        source_array = [east, northeast, north, northwest, west, southwest, south, southeast]
        return list(filter(None, source_array))


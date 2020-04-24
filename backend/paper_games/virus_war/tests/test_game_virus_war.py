"""Тестирование логики игры (класс VirusWar).
"""
from django.test import TestCase
import numpy as np
from virus_war.game import VirusWar


class GetNeighboringCells(TestCase):
    def setUp(self):
        h, w = 10, 10
        figure_order =[2, 1, 3]
        self.game = VirusWar(h, w, figure_order)
        self.func = self.game._VirusWar__get_neighboring_cells

    def test_corner_1(self):
        i, j = 0, 0
        expected = [(0, 1), (1, 0), (1, 1)]
        self.assertEqual(self.func(i, j), expected)

    def test_corner_2(self):
        i, j = 0, 9
        expected = [(0, 8), (1, 8), (1, 9)]
        self.assertEqual(self.func(i, j), expected)

    def test_corner_3(self):
        i, j = 9, 9
        expected = [(8, 9), (8, 8), (9, 8)]
        self.assertEqual(self.func(i, j), expected)

    def test_corner_4(self):
        i, j = 9, 0
        expected = [(9, 1), (8, 1), (8, 0)]
        self.assertEqual(self.func(i, j), expected)

    def test_side_1(self):
        i, j = 0, 3
        expected = [(0, 4), (0, 2), (1, 2), (1, 3), (1, 4)]
        self.assertEqual(self.func(i, j), expected)

    def test_side_2(self):
        i, j = 4, 9
        expected = [(3, 9), (3, 8), (4, 8), (5, 8), (5, 9)]
        self.assertEqual(self.func(i, j), expected)

    def test_side_3(self):
        i, j = 9, 7
        expected = [(9, 8), (8, 8), (8, 7), (8, 6), (9, 6)]
        self.assertEqual(self.func(i, j), expected)

    def test_side_4(self):
        i, j = 6, 0
        expected = [(6, 1), (5, 1), (5, 0), (7, 0), (7, 1)]
        self.assertEqual(self.func(i, j), expected)

    def test_inside_1(self):
        i, j = 5, 5
        expected = [(5, 6), (4, 6), (4, 5), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6)]
        self.assertEqual(self.func(i, j), expected)

    def test_inside_2(self):
        i, j = 2, 7
        expected = [(2, 8), (1, 8), (1, 7), (1, 6), (2, 6), (3, 6), (3, 7), (3, 8)]
        self.assertEqual(self.func(i, j), expected)


class ConnectedChainIsNearby(TestCase):
    def setUp(self):
        """
        Note:
            Количество игроков и размеры доски влияют на результат тестов!
            Первое число в figure_order - текущая фигура.
            Число -1 на доске обозначает тестируемую позицию (для наглядности)
        """
        h, w = 5, 5
        figure_order = np.array([2, 1, 3])
        self.game = VirusWar(h, w, figure_order)
        self.func = self.game._VirusWar__connected_chain_is_nearby


    def test_empty(self):
        self.game._board = [[0, 0, 0,  0, 0],
                            [0, 0, 0,  0, 0],
                            [0, 0, -1, 0, 0],
                            [0, 0, 0,  0, 0],
                            [0, 0, 0,  0, 0]]
        self.assertEqual(self.func(2, 2), False)

    def test_next_to_living_1(self):
        self.game._board = [[0,  3,  0, 0, 0],
                            [3,  1, 1, 2, 0],
                            [34, 3, 0, 0, -1],
                            [0,  0,  0, 0, 0],
                            [0,  0,  0, 0, 0]]
        self.assertEqual(self.func(2, 4), True)

    def test_next_to_living_2(self):
        self.game._board = [[0,  3,  0, 0, 0],
                            [3,  -1, 2, 0, 0],
                            [33, 34, 0, 0, 0],
                            [8,  0,  0, 0, 0],
                            [0,  2,  0, 0, 0]]
        self.assertEqual(self.func(1, 1), True)

    def test_next_to_reinfected_plus_1(self):
        self.game._board = [[0,  3,  0, 0, 0],
                            [3,  -1, 0, 0, 0],
                            [32, 34, 0, 0, 0],
                            [2,  0,  0, 0, 0],
                            [0,  2,  0, 0, 0]]
        self.assertEqual(self.func(1, 1), True)

    def test_next_to_reinfected_plus_2(self):
        self.game._board = [[0,  3,   0,  0, 0],
                            [3,  -1,  0,  0, 0],
                            [32, 34,  23, 0, 0],
                            [23,  2,  2,  0, 0],
                            [0,   2,  2,  0, 0]]
        self.assertEqual(self.func(1, 1), True)

    def test_next_to_reinfected_plus_3(self):
        self.game._board = [[0,  0,  0, 4,  -1],
                            [0,  0,  0, 32,  0],
                            [0,  0,  5, 42,  0],
                            [0,  0,  3, 52,  0],
                            [0,  0,  2, 0,   0]]
        self.assertEqual(self.func(0, 4), True)


    def test_next_to_reinfected_minus_1(self):
        self.game._board = [[0,  0,  0, 4,  -1],
                            [0,  0,  0, 32,  0],
                            [0,  0,  5, 42,  0],
                            [0,  0,  1, 52,  0],
                            [0,  0,  0, 0,   0]]
        self.assertEqual(self.func(0, 4), False)

    def test_next_to_reinfected_minus_2(self):
        self.game._board = [[0,  3,   0,  0, 0],
                            [3,  -1,  0,  0, 0],
                            [32, 34,  23, 0, 0],
                            [23,  3,  2,  0, 0],
                            [0,   2,  2,  0, 0]]
        self.assertEqual(self.func(1, 1), False)

    def test_hourse(self):
        self.game._board = [[2,   0,  0,    0, 0],
                            [0,   0,   4,    0, 0],
                            [0,   42,  42,  4, 0],
                            [0,   0,   4,    0, 4],
                            [0,   0,   4,    0, 4]]
        self.assertEqual(self.func(2, 3), False)

    def test_10x10(self):
        h, w = 10, 10
        figure_order = [4, 1]
        self.game = VirusWar(h, w, figure_order)
        self.func = self.game._VirusWar__connected_chain_is_nearby
        self.game._board = [[1, 0, 0, 0, 0, 0,   0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0,   0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0,   0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0,   0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0,   4, 0, 0, 0],
                            [0, 0, 0, 0, 1, 14,  41, 4, 0, 0],
                            [0, 0, 0, 0, 0, 1,   41, 4, 0, 0],
                            [0, 0, 0, 0, 0, 0,    1,  4, 0, 0],
                            [0, 0, 0, 0, 0, 41,  41,  4, 4, 0],
                            [0, 0, 0, 0, 0, 0,    0,  0, 0, 4]]
        self.assertEqual(self.func(6, 4), True)


class GetBlockedFigures(TestCase):
    def setUp(self):
        h, w = 5, 5
        figure_order = [1, 2, 3, 4]
        self.game = VirusWar(h, w, figure_order)
        self.func = self.game._VirusWar__get_blocked_figures

    def test_simple_block(self):
        self.game._board = [[1, 0, 1, 21, 2],
                            [1, 1, 1, 21, 21],
                            [1, 1, 1, 1, 1],
                            [1, 1, 42, 42, 42],
                            [1, 3, 43, 4,  42]]
        self.assertEqual(self.func(), [2, 4])

    def test_not_simple_block(self):
        self.game._board = [[1,  0,  21, 21,  2],
                            [13, 13, 21,  2, 21],
                            [4,  43, 21, 21,  2],
                            [13, 13, 21, 21,  2],
                            [1,   3, 31, 41,  2]]
        self.assertEqual(self.func(), [2, 4])

    def test_1_free(self):
        self.game._board = [[1,  31,  21, 21,  2],
                            [13, 13, 21,  2, 21],
                            [4,  43, 21, 21,  2],
                            [13, 13, 21, 21,  2],
                            [13,  31, 31, 41,  2]]
        self.assertEqual(self.func(), [2, 3, 4])


class RemoveFigure(TestCase):
    def setUp(self):
        h, w = 5, 5
        figure_order = [1, 2, 3, 4]
        self.game = VirusWar(h, w, figure_order)
        self.func = self.game.remove_figure

    def test_1(self):
        self.game._cur_index = 0
        self.game._cur_figure = 1
        remove_figure = 1
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 2})

    def test_2(self):
        self.game._cur_index = 0
        self.game._cur_figure = 1
        remove_figure = 2
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 1})

    def test_3(self):
        self.game._cur_index = 0
        self.game._cur_figure = 1
        remove_figure = 3
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 1})

    def test_4(self):
        self.game._cur_index = 0
        self.game._cur_figure = 1
        remove_figure = 4
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 1})

    def test_5(self):
        self.game._cur_index = 3
        self.game._cur_figure = 4
        remove_figure = 4
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 1})

    def test_6(self):
        self.game._cur_index = 3
        self.game._cur_figure = 4
        remove_figure = 3
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 4})

    def test_7(self):
        self.game._cur_index = 3
        self.game._cur_figure = 4
        remove_figure = 2
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 4})

    def test_8(self):
        self.game._cur_index = 2
        self.game._cur_figure = 3
        remove_figure = 3
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 4})

    def test_9(self):
        self.game._cur_index = 2
        self.game._cur_figure = 3
        remove_figure = 1
        self.assertEqual(self.func(remove_figure), {'game_over': False, 'cur_figure': 3})

    def test_10(self):
        self.game._cur_index = 2
        self.game._cur_figure = 3
        self.assertEqual(self.func(1), {'game_over': False, 'cur_figure': 3})
        self.assertEqual(self.func(4), {'game_over': False, 'cur_figure': 3})
        self.assertEqual(self.func(3), {'game_over': True, 'cur_figure': 2})


class TakeMove(TestCase):
    def setUp(self):
        h, w = 5, 5
        figure_order = [1, 2, 3, 4]
        self.game = VirusWar(h, w, figure_order)
        self.func = self.game.take_move

    def test_simple_move(self):
        self.game._cur_index = 2
        self.game._cur_figure = 3
        self.game._cur_stamina = 1
        self.game._board = [[1, 0, 1, 21, 2],
                            [1, 1, 1, 21, 21],
                            [1, 1, 1, 1, 1],
                            [1, 3, 42, 42, 42],
                            [1, 3, 43, 4,  42]]
        i, j = 2, 2
        expected = {'is_implemented': True, 'cell': 13, 'game_over':False, 'cur_figure': 1, 'blocked': [2, 4]}
        self.assertEqual(self.func(i, j), expected)
        self.assertEqual([1, 3], self.game._figure_order)

    def test_end_game(self):
        self.game._cur_index = 2
        self.game._cur_figure = 3
        self.game._cur_stamina = 1
        self.game._board = [[3, 0, 23, 23, 2],
                            [3, 3, 23, 23, 23],
                            [0, 0, 1, 1, 1],
                            [0, 3, 42, 42, 42],
                            [0, 3, 43, 4,  42]]
        i, j = 2, 2
        expected = {'is_implemented': True, 'cell': 13, 'game_over':True, 'cur_figure': 3, 'blocked': [1, 2, 4]}
        self.assertEqual(self.func(i, j), expected)
        self.assertEqual([3], self.game._figure_order)
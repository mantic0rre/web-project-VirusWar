"""Тестирование игрового движка (класс GameEngine).
"""
from django.test import TestCase
from django.contrib.auth.models import User
from virus_war.game.game_engine import *
from virus_war.models import Room


class Readiness(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='12345')
        self.user2 = User.objects.create(username='user2', password='12345')
        self.user3 = User.objects.create(username='user3', password='12345')
        self.user4 = User.objects.create(username='user4', password='12345')
        self.room1 = Room.objects.create(name='room1', max_players=3, height=10, width=10, owner=self.user1)
        self.room2 = Room.objects.create(name='room2', max_players=4, height=10, width=10, owner=self.user2)
        self.game_engine = Engine()
        self.func = self.game_engine.readiness
        self.running_games = self.game_engine._Engine__running_games
        self.ready_players = self.game_engine._Engine__ready_players

    def test_1_user_pos_confirm(self):
        state =  self.func(self.room1, self.user1, 1)
        expected_code = POS_CONFIRM
        expected_data = {'ready_players': {"user1": 1}, 'dirty': True}
        self.assertEqual(expected_code, state.dict['code'])
        self.assertEqual(expected_data, state.dict['data'])
        self.assertEqual({}, self.running_games)
        self.assertEqual({self.room1.id: expected_data['ready_players']}, self.ready_players)

    def test_2_users_pos_confirm(self):
        state = self.func(self.room1, self.user1, 1)
        state = self.func(self.room1, self.user2, 2)
        expected_code = POS_CONFIRM
        expected_data = {'ready_players': {"user1": 1, "user2": 2}, 'dirty': True}
        self.assertEqual(expected_code, state.dict['code'])
        self.assertEqual(expected_data, state.dict['data'])
        self.assertEqual({}, self.running_games)
        self.assertEqual({self.room1.id: expected_data['ready_players']}, self.ready_players)

    def test_max_users_game_start(self):
        state = self.func(self.room1, self.user1, 1)
        state = self.func(self.room1, self.user2, 2)
        state = self.func(self.room1, self.user3, 3)
        expected_code = GAME_START
        expected_data = {'ready_players': {"user1": 1, "user2": 2, "user3": 3}, 'dirty': True}
        self.assertEqual(expected_code, state.dict['code'])
        self.assertEqual(expected_data, state.dict['data'])
        self.assertEqual(1, len(self.running_games))
        self.assertEqual({self.room1.id: expected_data['ready_players']}, self.ready_players)

    def test_pos_change(self):
        state = self.func(self.room1, self.user1, 1)
        state = self.func(self.room1, self.user2, 2)
        state = self.func(self.room1, self.user1, 3)
        expected_code = POS_CHANGE
        expected_data = {'ready_players': {"user1": 3, "user2": 2}, 'dirty': True}
        self.assertEqual(expected_code, state.dict['code'])
        self.assertEqual(expected_data, state.dict['data'])
        self.assertEqual({}, self.running_games)
        self.assertEqual({self.room1.id: expected_data['ready_players']}, self.ready_players)

    def test_pos_denied(self):
        state = self.func(self.room1, self.user1, 1)
        state = self.func(self.room1, self.user2, 2)
        state = self.func(self.room1, self.user1, 2)
        expected_code = POS_DENIED
        expected_data = {'ready_players': {"user1": 1, "user2": 2}, 'dirty': False}
        self.assertEqual(expected_code, state.dict['code'])
        self.assertEqual(expected_data, state.dict['data'])
        self.assertEqual({}, self.running_games)
        self.assertEqual({self.room1.id: expected_data['ready_players']}, self.ready_players)

    def test_pos_cancel(self):
        state = self.func(self.room1, self.user1, 1)
        state = self.func(self.room1, self.user2, 2)
        state = self.func(self.room1, self.user1, 1)
        expected_code = POS_CANCEL
        expected_data = {'ready_players': {"user2": 2}, 'dirty': True}
        self.assertEqual(expected_code, state.dict['code'])
        self.assertEqual(expected_data, state.dict['data'])
        self.assertEqual({}, self.running_games)
        self.assertEqual({self.room1.id: expected_data['ready_players']}, self.ready_players)

    def test_pos_no_ready(self):
        state = self.func(self.room1, self.user1, 1)
        state = self.func(self.room1, self.user2, 2)
        state = self.func(self.room1, self.user1, 1)
        state = self.func(self.room1, self.user2, 2)
        expected_code = POS_NO_READY
        expected_data = {'ready_players': None, 'dirty': True}
        self.assertEqual(expected_code, state.dict['code'])
        self.assertEqual(expected_data, state.dict['data'])
        self.assertEqual({}, self.running_games)
        self.assertEqual({}, self.ready_players)


class EngineTakeMove(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='12345')
        self.user2 = User.objects.create(username='user2', password='12345')
        self.user3 = User.objects.create(username='user3', password='12345')
        self.user4 = User.objects.create(username='user4', password='12345')
        self.room1 = Room.objects.create(name='room1', max_players=4, height=5, width=5, owner=self.user1)
        self.game_engine = Engine()
        self.func = self.game_engine.take_move
        self.running_games = self.game_engine._Engine__running_games
        self.ready_players = self.game_engine._Engine__ready_players

    def test_end(self):
        pass

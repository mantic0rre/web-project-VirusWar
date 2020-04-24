"""Тестирование API пользователей.
"""
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class UsersAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.all().delete()

    def test_create(self):
        url = '/api/auth/users/'
        data = {'username': 'Test', 'password': 'ToniStark2020'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Test')
        self.assertEqual(response.data, {'email': '', 'username': 'Test', 'id': 1})

    def test_create_empty_username(self):
        url = '/api/auth/users/'
        data = {'username': '', 'password': 'ToniStark2020'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_empty_password(self):
        url = '/api/auth/users/'
        data = {'username': 'ToniStark', 'password': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_simple_password(self):
        url = '/api/auth/users/'
        data = {'username': 'ToniStark', 'password': '123qwerty'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_similar_password(self):
        url = '/api/auth/users/'
        data = {'username': 'ToniStark', 'password': 'ToniStark'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

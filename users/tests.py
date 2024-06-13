from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def test_register(self):
        response = self.client.post('/users/register/', {
            'email': 'user@testmail.com',
            'password': '123qwe456rty',
            'password2': '123qwe456rty',
            'tg_chat_id': 347214298
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='user@testmail.com').exists())

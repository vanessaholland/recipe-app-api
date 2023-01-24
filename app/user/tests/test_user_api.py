from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')


def create_test_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'testuserapi@example.com',
            'password': 'password_1',
            'name': 'Test APIUser'
        }

        result = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', result.data)

    def test_create_user_already_exists_error(self):
        payload = {
            'email': 'testuserapi@example.com',
            'password': 'password_1',
            'name': 'Test APIUser'
        }

        create_test_user(**payload)
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short(self):
        payload = {
            'email': 'testuserapi@example.com',
            'password': 'pw',
            'name': 'Test APIUser'
        }

        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user_auth(self):
        user_details = {
            'email': 'tokenuser@example.com',
            'password': 'testpass123',
            'name': 'Token APIUser'
        }
        create_test_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        result = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', result.data)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        create_test_user(email='mismatch@example.com',
                         password='good_password123')

        payload = {
            'email': 'mismatch@example.com',
            'password': 'bad_password123',
        }
        result = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', result.data)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_unathorized(self):
        result = self.client.get(ME_URL)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_test_user(
            email='mismatch@example.com',
            password='good_password123',
            name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_success(self):
        result = self.client.get(ME_URL)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, {
            'email': self.user.email,
            'name': self.user.name,
        })

    def test_post_not_allowed(self):
        result = self.client.post(ME_URL, {})

        self.assertEqual(result.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_user_success(self):
        payload = {'name': 'Updated Name', 'password': 'new_password_123'}

        result = self.client.patch(ME_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))

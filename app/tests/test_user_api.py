from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_sample_user(**params):
    """Creates sample user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """ Public tests for users API endpoints """

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'admin@admin.com',
            'password': 'password123',
            'name': 'name',
            'last_name': 'last_name'
        }

    def test_create_user_success(self):
        """ Test creating user successfully """
        res = self.client.post(CREATE_USER_URL, self.payload)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_invalid(self):
        """ Test creating invalid user """
        create_sample_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.payload['email'], res.data)

    def test_create_user_blank_fields(self):
        """ Test creating user with blank fields """
        data = {
            'email': '',
            'password': ''
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short(self):
        """ Test creating a user with invalid password """
        data = {
            'email': 'test@test.com',
            'password': 'pass'
        }
        res = self.client.post(CREATE_USER_URL, data)
        exists = get_user_model().objects.filter(
            email=data['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(exists)

    def test_create_token_for_user(self):
        """ Test token creation for user"""
        payload = {
            'email': 'email@teste.com',
            'password': 'test123'
        }
        create_sample_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test create user token with invalid credentials """
        create_sample_user(email='test@test.com', password='tesetee')
        payload = {
            'email': 'test@test.com',
            'password': 'incorrectpwd'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test token creation for non existing user """
        payload = {
            'email': 'email@teste.com',
            'password': 'senha123'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test creation of token with blank fields """
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

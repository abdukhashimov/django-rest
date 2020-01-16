from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# constants and helper functions
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """custom helper function to create user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successfull"""
        payload = {
            'email': 'test@gsoft.uz',
            'password': 'testpassword',
            'name': 'test full name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password, payload.get('password'))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a new user already exists"""
        payload = {
            'email': 'test@greatsoft.uz',
            'password': 'test123',
            'name': 'test name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must more than 5 characters"""
        payload = {
            'email': 'test@gsoft.uz',
            'password': 'max'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for the user"""
        payload = {
            'email': 'test@greatsoft.uz',
            'password': 'testpassword'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """Test that token is not created when invalid credentials are given"""
        create_user(email='test@greatsoft.uz', password='testpassword')
        payload = {
            'email':'te2st@greatsoft.uz',
            'password': 'abcasd'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """Test that token is not created when user does not exist"""
        payload = {
            'email': 'test@greatsoft.uz',
            'password': 'testpassword'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and passwords are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password':''})
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

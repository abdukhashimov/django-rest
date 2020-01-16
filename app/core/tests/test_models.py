from django.test import TestCase
from django.contrib.auth import get_user_model


def get_email_password():
    return 'test@greatsoft.uz', 'testpassword'


class ModelTest(TestCase):
    """Test the Custom User Model"""

    def test_create_user_with_email_successfull(self):
        """Test creating a new user with email successfull"""
        email, password = get_email_password()

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normilized(self):
        """Test creating a user with not normilized email"""
        email, password = get_email_password()
        temp = email.split('@')
        temp[1] = temp[1].upper()
        email = temp[0] + '@' + temp[1]
        del temp
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_user_with_invalid_email(self):
        """Test creating a new user with invalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='testpassword'
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email, password = get_email_password()
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
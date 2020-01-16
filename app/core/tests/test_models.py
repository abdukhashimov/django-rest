from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
# helper functions below


def get_email_password():
    return 'test@greatsoft.uz', 'testpassword'


def sample_user(email='test@greatsoft.uz', password='testpassword'):
    return get_user_model().objects.create_user(email=email, password=password)


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

    # Tag Model tests
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    # Test Ingridient model
    def test_ingredient_str(self):
        """Test the string representation of ingredient"""
        tag = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(tag), tag.name)

    # testing Recipe app
    def test_recipe_str(self):
        """Test the string representation of ingredient"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom souce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag

from recipe.serializers import TagSerializer


# constants
TAGS_URL = reverse('recipe:tag-list')


class PublicTagTest(TestCase):
    """Testing the .namepublicly available API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for users to retrive tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """Test authorized tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@greatsoft.uz',
            password='testpassword'
        )
        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """Test retriving for authenticated users"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@greatsoft.uz',
            'testpassword'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a tag using api"""
        payload = {'name':'Test Tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
    
    def test_create_tag_invalid(self):
        """Test creaating a tag with invaid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

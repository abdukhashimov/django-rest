from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test@admin.gsoft.uz',
            password='testpassword'
        )
        self.user = get_user_model().objects.create_user(
            email='test@gsoft.uz',
            password='testpassword',
            name='test full user name'
        )

        self.client.force_login(self.admin_user)

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_change_page(self):
        """User edit page workd"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        res =  self.client.get(url)
        
        self.assertEqual(res.status_code, 200)


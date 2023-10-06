from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='adminuser@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        url = reverse('admin:core_user_changelist')
        result = self.client.get(url)

        self.assertContains(result, self.user.email)
        self.assertContains(result, self.user.name)

    def test_user_edit_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)

    def test_user_create_page(self):
        url = reverse('admin:core_user_add')
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email(self):
        email = 'test@example.com'
        password = 'testpassword1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_emails_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'samplepass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_error_raises_error(self):
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user('', 'samplepass123')

    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(
            'superuser@example.com',
            'superpass123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

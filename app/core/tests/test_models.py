from django.test import TestCase
from django.contrib.auth import get_user_model

from core.factories import UserFactory


class ModelTests(TestCase):

    def test_user_has_valid_factory(self):
        user = UserFactory(
            email='me@gmail.com',
            password='12345678',
            name='Im me'
        )
        self.assertTrue(user.id is not None)

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = 'tests@test.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = 'tests@TEST.COM'
        user = get_user_model().objects.create_user(email=email,
                                                    password='Test12345')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'tests!23')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            email='tests@test.com',
            password='test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """ Class designed to test models from core app """

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with a email """

        email = 'admin@admin.com'
        password = 'password123'
        name = 'Admin'
        last_name = 'admin'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
            last_name=last_name
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, name)
        self.assertEqual(user.last_name, last_name)

    def test_create_user_with_normalized_email(self):
        """ Test creating a user with its email normalized """

        email = 'admin@ADMIN.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='password123',
            name='name',
            last_name='last_name'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating a user with a invalid email """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='password123',
                name='name',
                last_name='last_name'
            )

    def test_create_super_user(self):
        """ Test creating a superuser """

        user = get_user_model().objects.create_superuser(
            email='super@user.com',
            password='superpassword123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status


class AdminSiteTest(TestCase):
    ''' Class designed to test admin site features '''

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='normal@user.com',
            password='user_password123',
            name='normal',
            last_name='user'
        )
        self.admin = get_user_model().objects.create_superuser(
            email='super@user.com',
            password='super_user_password123'
        )
        self.client.force_login(self.admin)

    def test_user_listed(self):
        ''' Test user listing '''

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_edit_page(self):
        ''' Test edit user page '''

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_create_page(self):
        ''' Test create user page '''

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

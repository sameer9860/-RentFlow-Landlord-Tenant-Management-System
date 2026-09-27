from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CoreApiTests(TestCase):
    def test_auth_status_api_returns_authenticated_user_role(self):
        user = User.objects.create_user(username='landlord_core', password='StrongPass123')
        profile = user.profile
        profile.role = 'LANDLORD'
        profile.save()

        self.client.login(username='landlord_core', password='StrongPass123')
        response = self.client.get(reverse('core:auth-status'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_authenticated'])
        self.assertEqual(response.json()['role'], 'LANDLORD')

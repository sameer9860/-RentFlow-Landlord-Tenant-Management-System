from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class ProfileApiTests(TestCase):
    def test_profile_api_list_returns_profiles(self):
        user = User.objects.create_user(username='landlord1', password='StrongPass123')
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'LANDLORD', 'phone': '9800000000', 'address': 'Kathmandu'},
        )
        if created:
            profile.role = 'LANDLORD'
            profile.phone = '9800000000'
            profile.address = 'Kathmandu'
            profile.save()

        response = self.client.get(reverse('accounts:profile-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['user']['username'], 'landlord1')

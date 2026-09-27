from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Property, Room, Tenancy


class PropertyApiTests(TestCase):
    def test_property_api_list_returns_properties(self):
        user = User.objects.create_user(username='landlord2', password='StrongPass123')
        Property.objects.create(
            landlord=user,
            name='Sunset Apartments',
            address='Pokhara',
            description='Two-bedroom property',
        )

        response = self.client.get(reverse('properties:property-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Sunset Apartments')

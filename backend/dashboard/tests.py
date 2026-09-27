from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from payments.models import Expense, Payment, RentInvoice
from properties.models import Property, Room, Tenancy


class DashboardApiTests(TestCase):
    def setUp(self):
        self.landlord = User.objects.create_user(username='landlord', password='StrongPass123')
        self.tenant = User.objects.create_user(username='tenant', password='StrongPass123')
        self.landlord.profile.role = 'LANDLORD'
        self.landlord.profile.save()
        self.tenant.profile.role = 'TENANT'
        self.tenant.profile.save()

        self.property = Property.objects.create(
            landlord=self.landlord,
            name='Property One',
            address='Kathmandu',
            description='Test property',
        )
        self.room = Room.objects.create(
            property=self.property,
            room_number='101',
            monthly_rent=2000,
            capacity=2,
            is_active=True,
        )
        self.tenancy = Tenancy.objects.create(
            tenant=self.tenant,
            room=self.room,
            start_date='2024-01-01',
            end_date=None,
            is_active=True,
        )
        self.invoice = RentInvoice.objects.create(
            tenancy=self.tenancy,
            month=1,
            year=2024,
            amount=2000,
            due_date='2024-01-07',
            status='PAID',
        )
        Payment.objects.create(
            invoice=self.invoice,
            paid_amount=2000,
            method='CASH',
            transaction_id='TXN-001',
        )
        Expense.objects.create(
            landlord=self.landlord,
            category='MAINTENANCE',
            amount=300,
            description='Paint work',
        )

    def test_dashboard_summary_api_returns_values(self):
        self.client.login(username='landlord', password='StrongPass123')

        response = self.client.get(reverse('dashboard:dashboard-summary'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_properties'], 1)
        self.assertEqual(response.json()['total_rooms'], 1)
        self.assertEqual(response.json()['active_tenancies'], 1)
        self.assertEqual(float(response.json()['collected_income']), 2000.0)

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from properties.models import Property, Room, Tenancy
from .models import Expense, Payment, RentInvoice


class PaymentApiTests(TestCase):
    def setUp(self):
        self.landlord = User.objects.create_user(username='landlord1', password='StrongPass123')
        self.tenant = User.objects.create_user(username='tenant1', password='StrongPass123')
        self.landlord.profile.role = 'LANDLORD'
        self.landlord.profile.save()
        self.tenant.profile.role = 'TENANT'
        self.tenant.profile.save()

        self.property = Property.objects.create(
            landlord=self.landlord,
            name='Skyline Apartments',
            address='Kathmandu',
            description='Test property',
        )
        self.room = Room.objects.create(
            property=self.property,
            room_number='101',
            monthly_rent=1500,
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
            amount=1500,
            due_date='2024-01-07',
            status='PENDING',
        )
        self.payment = Payment.objects.create(
            invoice=self.invoice,
            paid_amount=1500,
            method='CASH',
            transaction_id='TXN-001',
        )
        self.expense = Expense.objects.create(
            landlord=self.landlord,
            category='MAINTENANCE',
            amount=250,
            description='Paint touch-up',
        )

    def test_invoice_api_list_returns_invoices(self):
        response = self.client.get(reverse('payments:invoice-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['tenant_name'], 'tenant1')

    def test_payment_api_list_returns_payment(self):
        response = self.client.get(reverse('payments:payment-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(float(response.json()[0]['paid_amount']), 1500.0)

    def test_expense_api_list_returns_expenses(self):
        response = self.client.get(reverse('payments:expense-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['category'], 'MAINTENANCE')

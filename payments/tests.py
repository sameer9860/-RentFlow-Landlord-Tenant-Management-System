from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from properties.models import Property, Room, Tenancy
from payments.models import RentInvoice, Payment


class PaymentConfirmationWorkflowTests(TestCase):
    def setUp(self):
        # create landlord and tenant users with profiles
        self.landlord = User.objects.create_user(username='landlord', password='pass')
        self.tenant = User.objects.create_user(username='tenant', password='pass')
        self.landlord.profile.role = 'LANDLORD'
        self.landlord.profile.save()
        self.tenant.profile.role = 'TENANT'
        self.tenant.profile.save()

        # create a property/room/tenancy
        prop = Property.objects.create(landlord=self.landlord, name='TestProp', address='123 St')
        room = Room.objects.create(property=prop, room_number='101', monthly_rent=1000)
        self.tenancy = Tenancy.objects.create(tenant=self.tenant, room=room, start_date='2024-01-01')

        # create an invoice
        self.invoice = RentInvoice.objects.create(
            tenancy=self.tenancy,
            month=1,
            year=2024,
            amount=1000,
            due_date='2024-01-07',
            status='PENDING'
        )

        self.client = Client()

    def test_tenant_can_submit_payment_and_invoice_awaits(self):
        # tenant logs in
        self.client.login(username='tenant', password='pass')
        url = reverse('payments:process_payment', kwargs={'pk': self.invoice.pk})
        resp = self.client.post(url, data={'method': 'CASH'})
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'AWAITING')
        payment = Payment.objects.filter(invoice=self.invoice).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.paid_amount, self.invoice.amount)

    def test_landlord_confirms_payment(self):
        # simulate tenant already paid
        Payment.objects.create(invoice=self.invoice, paid_amount=self.invoice.amount, method='CASH')
        self.invoice.status = 'AWAITING'
        self.invoice.save()

        self.client.login(username='landlord', password='pass')
        url = reverse('payments:mark_paid', kwargs={'pk': self.invoice.pk})
        resp = self.client.post(url)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'PAID')

    def test_generate_invoices_get_works(self):
        # ensure GET on generation endpoint triggers creation
        self.client.login(username='landlord', password='pass')
        self.invoice.delete()  # remove existing invoice
        url = reverse('payments:generate_invoices')
        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('payments:invoice_list'))
        self.assertTrue(RentInvoice.objects.filter(tenancy=self.tenancy, month=1, year=2024).exists())

    def test_landlord_confirms_payment(self):
        # simulate tenant already paid
        Payment.objects.create(invoice=self.invoice, paid_amount=self.invoice.amount, method='CASH')
        self.invoice.status = 'AWAITING'
        self.invoice.save()

        self.client.login(username='landlord', password='pass')
        url = reverse('payments:mark_paid', kwargs={'pk': self.invoice.pk})
        resp = self.client.post(url)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'PAID')

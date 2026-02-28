from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from datetime import date
from core.mixins import LandlordRequiredMixin
from properties.models import Tenancy
from .models import RentInvoice, Payment
from .forms import PaymentForm

class ProfileRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and hasattr(self.request.user, 'profile')

class InvoiceListView(ProfileRequiredMixin, ListView):
    model = RentInvoice
    template_name = 'payments/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        user = self.request.user
        qs = RentInvoice.objects.select_related('tenancy__room__property', 'tenancy__tenant')
        if user.profile.role == 'LANDLORD':
            return qs.filter(tenancy__room__property__landlord=user).order_by('-year', '-month')
        else:
            return qs.filter(tenancy__tenant=user).order_by('-year', '-month')

class GenerateInvoicesView(LandlordRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        today = timezone.now().date()
        month = today.month
        year = today.year
        
        # We only generate invoices for tenancies owned by this landlord
        active_tenancies = Tenancy.objects.filter(room__property__landlord=request.user, is_active=True)
        count = 0
        
        for tenancy in active_tenancies:
            invoice, created = RentInvoice.objects.get_or_create(
                tenancy=tenancy,
                month=month,
                year=year,
                defaults={
                    'amount': tenancy.room.monthly_rent,
                    'due_date': date(year, month, 7),
                    'status': 'PENDING'
                }
            )
            if created:
                count += 1
        
        if count > 0:
            messages.success(request, f"Successfully generated {count} new invoices for {month}/{year}.")
        else:
            messages.info(request, f"No new invoices to generate for {month}/{year}.")
            
        return redirect('payments:invoice_list')

class MarkInvoicePaidView(LandlordRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        invoice = RentInvoice.objects.filter(
            pk=pk,
            tenancy__room__property__landlord=request.user
        ).first()
        if invoice:
            invoice.status = 'PAID'
            invoice.save()
            messages.success(request, f"Invoice #{invoice.id} marked as paid.")
        else:
            messages.error(request, "Invoice not found or access denied.")
        return redirect('payments:invoice_list')

class InvoiceDetailView(ProfileRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        if user.profile.role == 'LANDLORD':
            invoice = RentInvoice.objects.filter(
                pk=pk,
                tenancy__room__property__landlord=user
            ).select_related('tenancy__room__property', 'tenancy__tenant').first()
        else:
            invoice = RentInvoice.objects.filter(
                pk=pk,
                tenancy__tenant=user
            ).select_related('tenancy__room__property', 'tenancy__tenant').first()
        if not invoice:
            messages.error(request, "Invoice not found.")
            return redirect('payments:invoice_list')
        
        context = {'invoice': invoice}
        if user.profile.role == 'TENANT' and invoice.status == 'PENDING':
            context['payment_form'] = PaymentForm()
            
        return render(request, 'payments/invoice_detail.html', context)

class ProcessPaymentView(ProfileRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        invoice = RentInvoice.objects.filter(
            pk=pk,
            tenancy__tenant=request.user,
            status='PENDING'
        ).first()

        if not invoice:
            messages.error(request, "Invoice not found or already paid.")
            return redirect('payments:invoice_list')

        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.paid_amount = invoice.amount
            payment.save()

            invoice.status = 'PAID'
            invoice.save()

            messages.success(request, f"Payment for Invoice #{invoice.id} processed successfully.")
            return redirect('payments:invoice_detail', pk=pk)
        
        messages.error(request, "Invalid payment details.")
        return redirect('payments:invoice_detail', pk=pk)

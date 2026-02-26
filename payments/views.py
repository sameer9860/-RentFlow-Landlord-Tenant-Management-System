from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from datetime import date
from core.mixins import LandlordRequiredMixin
from properties.models import Tenancy
from .models import RentInvoice

class ProfileRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and hasattr(self.request.user, 'profile')

class InvoiceListView(ProfileRequiredMixin, ListView):
    model = RentInvoice
    template_name = 'payments/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'LANDLORD':
            return RentInvoice.objects.filter(tenancy__room__property__landlord=user).order_by('-year', '-month')
        else:
            return RentInvoice.objects.filter(tenancy__tenant=user).order_by('-year', '-month')

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

from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
        if hasattr(user, 'profile') and user.profile.role == 'LANDLORD':
            return RentInvoice.objects.filter(tenancy__room__property__landlord=user).order_by('-year', '-month')
        else:
            return RentInvoice.objects.filter(tenancy__tenant=user).order_by('-year', '-month')

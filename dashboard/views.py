from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from core.mixins import LandlordRequiredMixin, TenantRequiredMixin
from properties.models import Property, Room, Tenancy
from payments.models import RentInvoice, Payment

class LandlordDashboardView(LandlordRequiredMixin, TemplateView):
    template_name = 'dashboard/landlord_dash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Stats
        context['total_properties'] = Property.objects.filter(landlord=user).count()
        context['total_rooms'] = Room.objects.filter(property__landlord=user).count()
        context['active_tenancies'] = Tenancy.objects.filter(room__property__landlord=user, is_active=True).count()
        context['vacant_rooms'] = context['total_rooms'] - context['active_tenancies']
        
        # Financials
        all_invoices = RentInvoice.objects.filter(tenancy__room__property__landlord=user)
        context['expected_income'] = all_invoices.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # only count payments for invoices that have been confirmed
        collected = Payment.objects.filter(
            invoice__tenancy__room__property__landlord=user,
            invoice__status='PAID'
        ).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        context['collected_income'] = collected
        context['pending_income'] = context['expected_income'] - collected
        
        total_rooms = context['total_rooms']
        active = context['active_tenancies']

        if context['total_rooms'] > 0:
            occupancy = (context['active_tenancies'] / context['total_rooms']) * 100
            context['occupancy_rate'] = round(occupancy, 2)
        else:
            context['occupancy_rate'] = 0.0
            
        return context

class TenantDashboardView(TenantRequiredMixin, TemplateView):
    template_name = 'dashboard/tenant_dash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Active Tenancy
        tenancy = Tenancy.objects.filter(tenant=user, is_active=True).first()
        context['tenancy'] = tenancy
        
        if tenancy:
            invoices = RentInvoice.objects.filter(tenancy=tenancy).order_by('-year', '-month')
            context['invoices'] = invoices
            
            total_due = invoices.aggregate(Sum('amount'))['amount__sum'] or 0
            total_paid = Payment.objects.filter(invoice__tenancy=tenancy).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
            
            context['outstanding_balance'] = total_due - total_paid
            
        return context

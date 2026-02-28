from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import TenantPasswordChangeForm

class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'profile'):
            # Enforce password change for new tenants
            if user.profile.needs_password_change:
                messages.info(request, "For security reasons, please change your password before continuing.")
                return redirect('accounts:password_change')

            if user.profile.role == 'LANDLORD':
                return redirect('dashboard:landlord_dash')
            elif user.profile.role == 'TENANT':
                return redirect('dashboard:tenant_dash')
        # Default or error case
        return redirect('admin:index')

class TenantPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = TenantPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:dashboard_redirect')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Clear the flag after successful password change
        profile = self.request.user.profile
        profile.needs_password_change = False
        profile.save()
        messages.success(self.request, "Password changed successfully! Welcome to RentFlow.")
        return response

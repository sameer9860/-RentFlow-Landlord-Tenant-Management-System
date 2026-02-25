from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'profile'):
            if user.profile.role == 'LANDLORD':
                return redirect('dashboard:landlord_dash')
            elif user.profile.role == 'TENANT':
                return redirect('dashboard:tenant_dash')
        # Default or error case
        return redirect('admin:index')

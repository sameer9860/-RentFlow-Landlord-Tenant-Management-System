from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class LandlordRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'LANDLORD'

class TenantRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'TENANT'

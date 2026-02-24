from django.urls import path
from .views import LandlordDashboardView, TenantDashboardView

app_name = 'dashboard'

urlpatterns = [
    path('landlord/', LandlordDashboardView.as_view(), name='landlord_dash'),
    path('tenant/', TenantDashboardView.as_view(), name='tenant_dash'),
]

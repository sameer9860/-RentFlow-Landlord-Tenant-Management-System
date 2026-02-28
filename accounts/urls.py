from django.urls import path
from .views import DashboardRedirectView, TenantPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('dashboard-redirect/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('password-change/', TenantPasswordChangeView.as_view(), name='password_change'),
]

from django.urls import path
from .views import DashboardRedirectView, TenantPasswordChangeView, profile_view

app_name = 'accounts'

urlpatterns = [
    path('', DashboardRedirectView.as_view(), name='dashboard_redirect_root'),
    path('dashboard-redirect/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('password-change/', TenantPasswordChangeView.as_view(), name='password_change'),
    path('profile/<int:profile_id>/', profile_view, name='profile_view'),
]

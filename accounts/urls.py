from django.urls import path
from .views import DashboardRedirectView

app_name = 'accounts'

urlpatterns = [
    path('', DashboardRedirectView.as_view(), name='dashboard_redirect_root'),
    path('dashboard-redirect/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
]

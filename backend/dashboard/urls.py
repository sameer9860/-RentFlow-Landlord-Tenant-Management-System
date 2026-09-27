from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import DashboardSummaryViewSet
from .views import LandlordDashboardView, TenantDashboardView

app_name = 'dashboard'

router = DefaultRouter()
router.register(r'api/dashboard', DashboardSummaryViewSet, basename='dashboard')

urlpatterns = [
    path('landlord/', LandlordDashboardView.as_view(), name='landlord_dash'),
    path('tenant/', TenantDashboardView.as_view(), name='tenant_dash'),
    path('', include(router.urls)),
]

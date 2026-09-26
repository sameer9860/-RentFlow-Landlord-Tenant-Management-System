from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import ProfileViewSet
from .views import DashboardRedirectView, TenantPasswordChangeView, profile_view

app_name = 'accounts'

router = DefaultRouter()
router.register(r'api/profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', DashboardRedirectView.as_view(), name='dashboard_redirect_root'),
    path('dashboard-redirect/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('password-change/', TenantPasswordChangeView.as_view(), name='password_change'),
    path('profile/<int:profile_id>/', profile_view, name='profile_view'),
    path('', include(router.urls)),
]

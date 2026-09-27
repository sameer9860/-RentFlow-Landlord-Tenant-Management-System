from django.urls import path

from .api import auth_status

app_name = 'core'

urlpatterns = [
    path('api/auth-status/', auth_status, name='auth-status'),
]

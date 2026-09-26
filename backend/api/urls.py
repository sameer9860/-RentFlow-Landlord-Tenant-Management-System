from django.urls import path
from .views import health_check, dashboard_summary, property_list, room_list, tenancy_list, invoice_list, expense_list

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('dashboard/summary/', dashboard_summary, name='dashboard_summary'),
    path('properties/', property_list, name='api_property_list'),
    path('rooms/', room_list, name='api_room_list'),
    path('tenancies/', tenancy_list, name='api_tenancy_list'),
    path('invoices/', invoice_list, name='api_invoice_list'),
    path('expenses/', expense_list, name='api_expense_list'),
]

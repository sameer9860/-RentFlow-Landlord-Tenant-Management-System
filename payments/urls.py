from django.urls import path
from .views import InvoiceListView

app_name = 'payments'

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
]

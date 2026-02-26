from django.urls import path
from .views import InvoiceListView, GenerateInvoicesView

app_name = 'payments'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('generate-invoices/', GenerateInvoicesView.as_view(), name='generate_invoices'),
]

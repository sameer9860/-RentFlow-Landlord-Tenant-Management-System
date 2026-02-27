from django.urls import path
from .views import InvoiceListView, GenerateInvoicesView, MarkInvoicePaidView, InvoiceDetailView

app_name = 'payments'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('generate-invoices/', GenerateInvoicesView.as_view(), name='generate_invoices'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('<int:pk>/mark-paid/', MarkInvoicePaidView.as_view(), name='mark_paid'),
]

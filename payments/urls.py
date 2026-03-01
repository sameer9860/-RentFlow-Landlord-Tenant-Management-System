from django.urls import path
from .views import (
    InvoiceListView, GenerateInvoicesView, MarkInvoicePaidView, 
    InvoiceDetailView, ProcessPaymentView,
    ExpenseListView, ExpenseCreateView, FinancialReportView,
    ExportReportPDFView, ExportReportCSVView
)

app_name = 'payments'

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/generate/', GenerateInvoicesView.as_view(), name='generate_invoices'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:pk>/pay/', ProcessPaymentView.as_view(), name='process_payment'),
    path('invoices/<int:pk>/mark-paid/', MarkInvoicePaidView.as_view(), name='mark_paid'),
    
    # Expenses
    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', ExpenseCreateView.as_view(), name='expense_create'),
    
    # Reports
    path('reports/monthly/', FinancialReportView.as_view(), name='financial_report'),
    path('reports/monthly/pdf/', ExportReportPDFView.as_view(), name='export_report_pdf'),
    path('reports/monthly/csv/', ExportReportCSVView.as_view(), name='export_report_csv'),
]

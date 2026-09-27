from rest_framework import permissions, viewsets

from .models import Expense, Payment, RentInvoice
from .serializers import ExpenseSerializer, InvoiceSerializer, PaymentSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = RentInvoice.objects.select_related('tenancy__tenant', 'tenancy__room__property').all().order_by('-year', '-month', '-id')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.AllowAny]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice__tenancy__tenant').all().order_by('-id')
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('landlord').all().order_by('-date', '-id')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.AllowAny]

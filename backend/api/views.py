from django.db.models import Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from payments.models import RentInvoice, Payment, Expense
from properties.models import Property, Room, Tenancy
from .serializers import PropertySerializer, RoomSerializer, TenancySerializer, InvoiceSerializer, ExpenseSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok", "message": "Django DRF API is running"})


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_summary(request):
    total_properties = Property.objects.count()
    total_rooms = Room.objects.count()
    active_tenancies = Tenancy.objects.filter(is_active=True).count()
    income = RentInvoice.objects.aggregate(total=Sum('amount'))['total'] or 0
    collected = Payment.objects.aggregate(total=Sum('paid_amount'))['total'] or 0
    expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    due = RentInvoice.objects.filter(status__in=['PENDING', 'AWAITING']).aggregate(total=Sum('amount'))['total'] or 0

    month = timezone.now().month
    year = timezone.now().year
    monthly_income = Payment.objects.filter(payment_date__month=month, payment_date__year=year).aggregate(total=Sum('paid_amount'))['total'] or 0
    monthly_expenses = Expense.objects.filter(date__month=month, date__year=year).aggregate(total=Sum('amount'))['total'] or 0
    monthly_due = RentInvoice.objects.filter(month=month, year=year, status__in=['PENDING', 'AWAITING']).aggregate(total=Sum('amount'))['total'] or 0

    return Response({
        'total_properties': total_properties,
        'total_rooms': total_rooms,
        'active_tenancies': active_tenancies,
        'income': float(income),
        'collected': float(collected),
        'expenses': float(expenses),
        'due': float(due),
        'monthly_income': float(monthly_income),
        'monthly_expenses': float(monthly_expenses),
        'monthly_due': float(monthly_due),
        'net_profit': float(monthly_income - monthly_expenses),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def property_list(request):
    properties = Property.objects.all().order_by('-id')
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def room_list(request):
    rooms = Room.objects.select_related('property').all().order_by('-id')
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def tenancy_list(request):
    tenancies = Tenancy.objects.select_related('tenant', 'room__property').all().order_by('-id')
    serializer = TenancySerializer(tenancies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def invoice_list(request):
    invoices = RentInvoice.objects.select_related('tenancy__tenant', 'tenancy__room__property').all().order_by('-year', '-month', '-id')
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date', '-id')
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

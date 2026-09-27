from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from payments.models import Expense, Payment, RentInvoice
from properties.models import Property, Room, Tenancy
from .serializers import DashboardSummarySerializer


class DashboardSummaryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=401)

        total_properties = Property.objects.filter(landlord=user).count()
        total_rooms = Room.objects.filter(property__landlord=user).count()
        active_tenancies = Tenancy.objects.filter(room__property__landlord=user, is_active=True).count()
        vacant_rooms = total_rooms - active_tenancies

        all_invoices = RentInvoice.objects.filter(tenancy__room__property__landlord=user)
        expected_income = all_invoices.aggregate(total=Sum('amount'))['total'] or Decimal('0')

        collected = Payment.objects.filter(
            invoice__tenancy__room__property__landlord=user,
            invoice__status='PAID',
        ).aggregate(total=Sum('paid_amount'))['total'] or Decimal('0')

        pending_income = expected_income - collected

        occupancy_rate = 0.0
        if total_rooms:
            occupancy_rate = round((active_tenancies / total_rooms) * 100, 2)

        today = timezone.now().date()
        month = today.month
        year = today.year

        invoices_month = all_invoices.filter(month=month, year=year)
        payments_month = Payment.objects.filter(
            invoice__tenancy__room__property__landlord=user,
            invoice__status='PAID',
            payment_date__month=month,
            payment_date__year=year,
        )
        expenses_month = Expense.objects.filter(
            landlord=user,
            date__month=month,
            date__year=year,
        )

        dash_revenue = payments_month.aggregate(total=Sum('paid_amount'))['total'] or Decimal('0')
        dash_expenses = expenses_month.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        dash_profit = dash_revenue - dash_expenses
        dash_due = invoices_month.filter(status__in=['PENDING', 'AWAITING']).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        payload = {
            'total_properties': total_properties,
            'total_rooms': total_rooms,
            'active_tenancies': active_tenancies,
            'vacant_rooms': vacant_rooms,
            'expected_income': expected_income,
            'collected_income': collected,
            'pending_income': pending_income,
            'occupancy_rate': occupancy_rate,
            'dash_revenue': dash_revenue,
            'dash_expenses': dash_expenses,
            'dash_profit': dash_profit,
            'dash_due': dash_due,
        }

        serializer = DashboardSummarySerializer(payload)
        return Response(serializer.data)

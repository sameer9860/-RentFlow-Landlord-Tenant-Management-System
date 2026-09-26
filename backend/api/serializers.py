from rest_framework import serializers
from properties.models import Property, Room, Tenancy
from payments.models import RentInvoice, Payment, Expense


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'name', 'address', 'description', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'property', 'property_name', 'room_number', 'monthly_rent', 'capacity', 'is_active']


class TenancySerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    property_name = serializers.CharField(source='room.property.name', read_only=True)

    class Meta:
        model = Tenancy
        fields = ['id', 'tenant', 'tenant_name', 'room', 'room_number', 'property_name', 'start_date', 'end_date', 'is_active']


class InvoiceSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenancy.tenant.username', read_only=True)
    room_number = serializers.CharField(source='tenancy.room.room_number', read_only=True)
    property_name = serializers.CharField(source='tenancy.room.property.name', read_only=True)

    class Meta:
        model = RentInvoice
        fields = ['id', 'tenancy', 'tenant_name', 'room_number', 'property_name', 'month', 'year', 'amount', 'due_date', 'status']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'paid_amount', 'payment_date', 'method', 'transaction_id']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date', 'description']

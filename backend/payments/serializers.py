from django.contrib.auth.models import User
from rest_framework import serializers

from properties.models import Property, Room, Tenancy
from .models import Expense, Payment, RentInvoice


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PropertySerializer(serializers.ModelSerializer):
    landlord = UserSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'landlord', 'name', 'address', 'description', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'property', 'room_number', 'monthly_rent', 'capacity', 'is_active']


class TenancySerializer(serializers.ModelSerializer):
    tenant = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Tenancy
        fields = ['id', 'tenant', 'room', 'start_date', 'end_date', 'is_active']


class InvoiceSerializer(serializers.ModelSerializer):
    tenancy = TenancySerializer(read_only=True)
    tenant_name = serializers.CharField(source='tenancy.tenant.username', read_only=True)
    room_number = serializers.CharField(source='tenancy.room.room_number', read_only=True)
    property_name = serializers.CharField(source='tenancy.room.property.name', read_only=True)

    class Meta:
        model = RentInvoice
        fields = [
            'id',
            'tenancy',
            'tenant_name',
            'room_number',
            'property_name',
            'month',
            'year',
            'amount',
            'due_date',
            'status',
            'generated_at',
        ]


class PaymentSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'paid_amount', 'payment_date', 'method', 'transaction_id']


class ExpenseSerializer(serializers.ModelSerializer):
    landlord = UserSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'landlord', 'category', 'amount', 'date', 'description', 'created_at']

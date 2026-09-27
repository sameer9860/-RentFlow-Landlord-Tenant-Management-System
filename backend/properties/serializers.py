from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Property, Room, Tenancy


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PropertySerializer(serializers.ModelSerializer):
    landlord = UserSummarySerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'landlord',
            'name',
            'address',
            'description',
            'created_at',
        ]


class RoomSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name', read_only=True)

    class Meta:
        model = Room
        fields = [
            'id',
            'property',
            'property_name',
            'room_number',
            'monthly_rent',
            'capacity',
            'is_active',
            'created_at',
        ]


class TenancySerializer(serializers.ModelSerializer):
    tenant = UserSummarySerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Tenancy
        fields = [
            'id',
            'tenant',
            'room',
            'start_date',
            'end_date',
            'is_active',
        ]

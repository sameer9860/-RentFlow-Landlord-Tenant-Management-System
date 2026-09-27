from rest_framework import permissions, viewsets

from .models import Property, Room, Tenancy
from .serializers import PropertySerializer, RoomSerializer, TenancySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.select_related('landlord').all().order_by('-id')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('property').all().order_by('-id')
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


class TenancyViewSet(viewsets.ModelViewSet):
    queryset = Tenancy.objects.select_related('tenant', 'room', 'room__property').all().order_by('-id')
    serializer_class = TenancySerializer
    permission_classes = [permissions.AllowAny]

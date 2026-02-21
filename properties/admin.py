from django.contrib import admin
from .models import Property, Room, Tenancy

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

class TenancyInline(admin.TabularInline):
    model = Tenancy
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'landlord', 'created_at')
    search_fields = ('name', 'landlord__username', 'address')
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'property', 'monthly_rent', 'is_active')
    list_filter = ('property', 'is_active')
    search_fields = ('room_number', 'property__name')
    inlines = [TenancyInline]

@admin.register(Tenancy)
class TenancyAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'room', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('tenant__username', 'room__room_number', 'room__property__name')

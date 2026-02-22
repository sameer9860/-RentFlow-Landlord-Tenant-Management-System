from django.contrib import admin
from .models import RentInvoice, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

@admin.register(RentInvoice)
class RentInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenancy', 'month', 'year', 'amount', 'due_date', 'status', 'generated_at')
    list_filter = ('status', 'month', 'year', 'due_date')
    search_fields = ('tenancy__tenant__username', 'tenancy__property__name', 'tenancy__room__room_number')
    inlines = [PaymentInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'paid_amount', 'payment_date', 'method', 'transaction_id')
    list_filter = ('method', 'payment_date')
    search_fields = ('invoice__id', 'transaction_id')


from payment.models import *
from django.contrib import admin

@admin.register(RoomPayment)
class RoomPaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'invoice_number', 'status', 'created_at', 'updated_at')
    search_fields = ('invoice_number', 'booking__user__name', 'booking__room__name')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

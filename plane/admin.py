from plane.models import *
from django.contrib import admin

@admin.register(PlaneBooking)
class PlaneBookingAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'origin',
        'destination',
        'trip_type',
        'travel_class',
        'departure_date',
        'return_date',
        'num_adults',
        'num_children',
        'num_infants',
        'created_at',
    )
    list_filter = (
        'trip_type',
        'travel_class',
        'departure_date',
        'return_date',
        'created_at',
    )
    search_fields = (
        'full_name',
        'email',
        'phone_number',
        'origin',
        'destination',
    )
    readonly_fields = ('created_at',)
    ordering = ['-created_at']

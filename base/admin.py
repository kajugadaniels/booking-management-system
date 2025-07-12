from base.models import *
from django.contrib import admin

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'created_at')
    readonly_fields = ('created_at',)
    def has_add_permission(self, request):
        # Prevent more than one instance
        return not Setting.objects.exists()

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at',)

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    readonly_fields = ['uploaded_at']

class RoomAmenityInline(admin.TabularInline):
    model = RoomAmenity
    extra = 1

class RoomReviewInline(admin.TabularInline):
    model = RoomReview
    extra = 0
    readonly_fields = ['user', 'rating', 'title', 'review', 'created_at']
    can_delete = False

@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'room_type', 'occupancy', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'hotel', 'room_type', 'occupancy')
    search_fields = ('name', 'hotel__name', 'room_type')
    list_per_page = 10
    inlines = [RoomImageInline, RoomAmenityInline, RoomReviewInline]

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name',)
from car.models import *
from django.contrib import admin

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    readonly_fields = ('uploaded_at',)
    show_change_link = False

class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 1
    autocomplete_fields = ['feature']
    show_change_link = False

class CarReviewInline(admin.StackedInline):
    model = CarReview
    extra = 0
    readonly_fields = ('user', 'rating', 'title', 'review', 'created_at')
    can_delete = False
    show_change_link = False

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_type', 'condition', 'fuel_type', 'price_per_day', 'is_available', 'created_at')
    list_filter = ('car_type', 'condition', 'fuel_type', 'transmission', 'color', 'is_available')
    search_fields = ('name', 'body', 'description')
    readonly_fields = ('created_at',)
    inlines = [CarImageInline, CarFeatureInline, CarReviewInline]
    autocomplete_fields = ['car_type']

@admin.register(CarBooking)
class CarBookingAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'pickup_date', 'dropoff_date', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'pickup_date', 'dropoff_date')
    search_fields = ('car__name', 'user__email', 'pickup_location', 'dropoff_location')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'caption', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    search_fields = ('car__name',)

@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'title', 'created_at')
    search_fields = ('car__name', 'user__email', 'title')
    readonly_fields = ('created_at',)

@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = ('car', 'feature')
    search_fields = ('car__name', 'feature__name')
    autocomplete_fields = ['car', 'feature']
    list_filter = ('feature',)
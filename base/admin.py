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
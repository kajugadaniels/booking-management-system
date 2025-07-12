from user.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('room-booking/', roomBooking, name="roomBooking"),
    path('car-booking/', carBooking, name="carBooking"),
    path('profile/', profile, name="profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
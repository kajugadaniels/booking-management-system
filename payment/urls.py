from payment.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'payment'

urlpatterns = [
    path('room/<str:invoice_number>/pay/', payRoomBooking, name='payRoomBooking'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
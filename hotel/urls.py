from hotel.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'hotel'

urlpatterns = [
    path('', getHotels, name="getHotels"),
    path('hotel/<int:hotel_id>/rooms/', hotelRooms, name="hotelRooms"),
    path('hotel/<int:hotel_id>/room/<int:room_id>/', roomDetails, name="roomDetails"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
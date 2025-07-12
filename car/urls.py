from car.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'car'

urlpatterns = [
    path('', getCars, name="getCars"),
    path('car/1/', carDetails, name="carDetails"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
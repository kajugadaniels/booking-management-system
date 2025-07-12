from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', include('base.urls')),
    path('admin/', admin.site.urls),
    path('cars/', include('car.urls')),
    path('users/', include('user.urls')),
    path('auth/', include('account.urls')),
    path('hotels/', include('hotel.urls')),
    path('planes/', include('plane.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'base.views.custom_404_view'
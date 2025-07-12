from base.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('how-it-works/', howItWorks, name="howItWorks"),
    path('privacy-policy/', privacyPolicy, name="privacyPolicy"),
    path('contact-us/', contact, name="contact"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
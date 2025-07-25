from account.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'auth'

urlpatterns = [
    path('register/', getRegister, name="getRegister"),
    path('login/', getLogin, name="getLogin"),
    path('logout/', logoutUser, name="getLogout"),
    path('forget-password/', forgetPassword, name="forgetPassword"),
    path('reset-password/<str:email>/', resetPassword, name="resetPassword"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from base.models import *
from django.shortcuts import render, redirect

def getLogin(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/auth/login.html', context)

def getRegister(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/auth/register.html', context)

def forgetPassword(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/auth/forget-password.html', context)
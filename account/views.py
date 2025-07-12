from base.models import *
from django.shortcuts import render, redirect

def getLogin(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/auth/login.html', context)

def getRegister(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/auth/register.html', context)

def forgetPassword(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/auth/forget-password.html', context)
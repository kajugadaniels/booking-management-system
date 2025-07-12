from base.models import *
from django.shortcuts import render, redirect

def dashboard(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/user/dashboard.html', context)

def roomBooking(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/user/rooms/index.html', context)
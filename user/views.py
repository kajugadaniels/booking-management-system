from base.models import *
from django.shortcuts import render, redirect

def dashboard(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/dashboard.html', context)

def roomBooking(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/rooms/index.html', context)

def carBooking(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/cars/index.html', context)

def profile(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/profile.html', context)
from base.models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/dashboard.html', context)

@login_required
def roomBooking(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/rooms/index.html', context)

@login_required
def carBooking(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/cars/index.html', context)

@login_required
def profile(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/profile.html', context)

@login_required
def changePassword(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/change-password.html', context)
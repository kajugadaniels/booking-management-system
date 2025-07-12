from base.models import *
from django.shortcuts import render, redirect

def getCars(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/cars/index.html', context)

def carDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/cars/show.html', context)
from base.models import *
from django.shortcuts import render, redirect

def getCars(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/cars/index.html', context)

def carDetails(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/cars/show.html', context)
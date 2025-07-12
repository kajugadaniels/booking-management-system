from base.models import *
from django.shortcuts import render, redirect

def getHotels(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/hotels/index.html', context)

def hotelRooms(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/hotels/rooms/index.html', context)

def roomDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/hotels/rooms/show.html', context)
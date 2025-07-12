from base.models import *
from django.shortcuts import render, redirect

def getHotels(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/hotels/index.html', context)

def hotelRooms(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/hotels/rooms/index.html', context)

def roomDetails(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/hotels/rooms/show.html', context)
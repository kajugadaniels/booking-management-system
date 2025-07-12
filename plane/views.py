from base.models import *
from django.shortcuts import render, redirect

def getPlanes(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/planes/index.html', context)
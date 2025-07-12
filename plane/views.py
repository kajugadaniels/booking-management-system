from base.models import *
from django.shortcuts import render, redirect

def getPlanes(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/planes/index.html', context)
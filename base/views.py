from base.models import *
from django.shortcuts import render, redirect

def home(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/index.html', context)
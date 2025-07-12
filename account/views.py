from base.models import *
from django.shortcuts import render, redirect

def getLogin(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/auth/login.html', context)
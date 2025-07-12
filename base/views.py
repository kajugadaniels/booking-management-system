from base.models import *
from django.shortcuts import render, redirect

def home(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/index.html', context)

def howItWorks(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/how-it-works.html', context)

def privacyPolicy(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/privacy-policy.html', context)

def contact(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings
    }

    return render (request, 'pages/contact.html', context)

def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)
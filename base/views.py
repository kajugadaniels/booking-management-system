from base.models import *
from django.shortcuts import render, redirect

def home(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/index.html', context)

def howItWorks(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/how-it-works.html', context)

def privacyPolicy(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/privacy-policy.html', context)

def contact(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/contact.html', context)

def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)
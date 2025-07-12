from base.forms import *
from base.models import *
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

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
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Email to user
            user_subject = "Pluto Booking — We've received your message"
            user_message = render_to_string('emails/contact_confirmation.html', {
                'contact': contact,
                'settings': site_settings,
            })
            send_mail(
                user_subject,
                '',
                settings.EMAIL_HOST_USER,
                [contact.email],
                html_message=user_message
            )

            # Email to admin
            if site_settings and site_settings.email:
                admin_subject = "Pluto Booking — New contact message"
                admin_message = render_to_string('emails/contact_admin_notification.html', {
                    'contact': contact,
                    'settings': site_settings,
                })
                send_mail(
                    admin_subject,
                    '',
                    settings.EMAIL_HOST_USER,
                    [site_settings.email],
                    html_message=admin_message
                )

            messages.success(request, "Thank you! We've received your message.")
            return redirect('base:contact')
        else:
            messages.error(request, "Please correct the errors and try again.")

    contact = {
        'settings': site_settings,
        'form': form
    }

    return render(request, 'pages/contact.html', contact)

def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)
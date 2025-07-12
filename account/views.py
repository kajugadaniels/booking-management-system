from base.models import *
from account.forms import *
from account.models import *
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

def getLogin(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/auth/login.html', context)

def getRegister(request):
    from base.models import Setting
    site_settings = Setting.objects.first()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'User'
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Send welcome email
            subject = 'Welcome to Pluto Booking!'
            message = render_to_string('emails/welcome.html', {
                'user': user,
                'settings': site_settings
            })
            send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=message)

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('auth:getLogin')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    context = {
        'settings': site_settings,
        'form': form,
    }

    return render(request, 'pages/auth/register.html', context)

def forgetPassword(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/auth/forget-password.html', context)
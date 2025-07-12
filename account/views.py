import random
from base.models import *
from account.forms import *
from account.models import *
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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

def getLogin(request):
    from base.models import Setting
    site_settings = Setting.objects.first()

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('base:home')  # Or any other landing page
        else:
            messages.error(request, "Login failed. Please check your credentials.")
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'settings': site_settings
    }

    return render(request, 'pages/auth/login.html', context)

@login_required
def logoutUser(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('auth:getLogin')

def forgetPassword(request):
    site_settings = Setting.objects.first()
    context = {
        'settings': site_settings
    }

    email_form = PasswordResetRequestForm()
    otp_form = OTPVerificationForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'send_otp':
            email_form = PasswordResetRequestForm(request.POST)
            if email_form.is_valid():
                email = email_form.cleaned_data['email']
                try:
                    user = User.objects.get(email=email)
                    otp = f"{random.randint(100000, 999999)}"
                    user.reset_otp = otp
                    user.otp_created_at = timezone.now()
                    user.save()

                    subject = 'Pluto Booking - Reset Your Password'
                    message = render_to_string('emails/reset_otp.html', {
                        'user': user,
                        'otp': otp,
                        'settings': site_settings
                    })
                    send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=message)

                    messages.success(request, f"OTP sent to {user.email}. Please check your inbox.")
                    context['step'] = 'verify'
                    context['email'] = user.email
                except User.DoesNotExist:
                    messages.error(request, "No user found with this email.")

        elif action == 'verify_otp':
            otp_form = OTPVerificationForm(request.POST)
            if otp_form.is_valid():
                email = otp_form.cleaned_data['email']
                otp = otp_form.cleaned_data['otp']
                new_password = otp_form.cleaned_data['new_password']
                confirm_password = otp_form.cleaned_data['confirm_password']

                try:
                    user = User.objects.get(email=email, reset_otp=otp)
                    if timezone.now() - user.otp_created_at > timedelta(minutes=10):
                        messages.error(request, "OTP has expired.")
                    elif new_password != confirm_password:
                        messages.error(request, "Passwords do not match.")
                    else:
                        user.set_password(new_password)
                        user.reset_otp = None
                        user.otp_created_at = None
                        user.save()
                        messages.success(request, "Password updated successfully. Please log in.")
                        return redirect('auth:getLogin')
                except User.DoesNotExist:
                    messages.error(request, "Invalid OTP or email.")

            context['step'] = 'verify'
            context['email'] = request.POST.get('email')

    context['email_form'] = email_form
    context['otp_form'] = otp_form

    return render(request, 'pages/auth/forget-password.html', context)
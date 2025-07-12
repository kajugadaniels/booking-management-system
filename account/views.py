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
    form = PasswordResetRequestForm()

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = f"{random.randint(100000, 999999)}"
                user.reset_otp = otp
                user.otp_created_at = timezone.now()
                user.save()

                subject = 'Pluto Booking - Password Reset OTP'
                message = render_to_string('emails/reset_otp.html', {
                    'user': user,
                    'otp': otp,
                    'settings': site_settings,
                })
                send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=message)

                messages.success(request, f"OTP has been sent to {user.email}.")
                return redirect('auth:resetPassword', email=user.email)
            except User.DoesNotExist:
                messages.error(request, "No account found with this email.")

    context = {
        'form': form,
        'settings': site_settings
    }

    return render(request, 'pages/auth/forget-password.html', context)

def resetPassword(request, email):
    site_settings = Setting.objects.first()
    form = OTPVerificationForm()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "Invalid password reset link.")
        return redirect('auth:forgetPassword')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if user.reset_otp != otp:
                messages.error(request, "Invalid OTP.")
            elif timezone.now() - user.otp_created_at > timedelta(minutes=10):
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

    context = {
        'form': form,
        'email': email,
        'settings': site_settings
    }

    return render(request, 'pages/auth/reset-password.html', context)

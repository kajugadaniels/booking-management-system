from user.forms import *
from base.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout

@login_required
def dashboard(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/dashboard.html', context)

@login_required
def roomBooking(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/rooms/index.html', context)

@login_required
def carBooking(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/cars/index.html', context)

@login_required
def planeBooking(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/user/planes/index.html', context)

@login_required
def profile(request):
    site_settings = Setting.objects.first()
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=user)

    context = {
        'settings': site_settings,
        'form': form,
    }

    return render(request, 'pages/user/profile.html', context)

@login_required
def changePassword(request):
    site_settings = Setting.objects.first()
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=user)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()

            # Log out user and redirect to login
            logout(request)
            messages.success(request, "Password updated successfully. Please log in with your new password.")
            return redirect('auth:getLogin')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ChangePasswordForm(user=user)

    context = {
        'settings': site_settings,
        'form': form,
    }

    return render(request, 'pages/user/change-password.html', context)
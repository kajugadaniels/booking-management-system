from user.forms import *
from car.models import *
from base.models import *
from plane.models import *
from hotel.models import *
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout


@login_required
def dashboard(request):
    site_settings = Setting.objects.first()

    user = request.user

    total_car_bookings = CarBooking.objects.filter(user=user).count()
    total_room_bookings = RoomBooking.objects.filter(user=user).count()
    total_plane_bookings = PlaneBooking.objects.filter(user=user).count()

    # Placeholder values for future features
    total_favorites = 0
    total_saved_searches = 0
    total_messages = 0

    context = {
        'settings': site_settings,
        'total_car_bookings': total_car_bookings,
        'total_room_bookings': total_room_bookings,
        'total_plane_bookings': total_plane_bookings,
        'total_favorites': total_favorites,
        'total_saved_searches': total_saved_searches,
        'total_messages': total_messages,
    }

    return render(request, 'pages/user/dashboard.html', context)

@login_required
def roomBooking(request):
    site_settings = Setting.objects.first()

    # Get search query and sorting option from GET params
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    bookings = RoomBooking.objects.filter(user=request.user)

    if query:
        bookings = bookings.filter(
            Q(room__name__icontains=query) |
            Q(room__hotel__name__icontains=query)
        )

    # Sorting
    if sort_by == 'oldest':
        bookings = bookings.order_by('created_at')
    else:
        bookings = bookings.order_by('-created_at')

    paginator = Paginator(bookings, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': site_settings,
        'bookings': page_obj,
        'query': query,
        'sort_by': sort_by,
    }

    return render(request, 'pages/user/rooms/index.html', context)

@login_required
def carBooking(request):
    site_settings = Setting.objects.first()

    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    bookings = CarBooking.objects.filter(user=request.user)

    if query:
        bookings = bookings.filter(
            Q(car__name__icontains=query) |
            Q(car__car_brand__name__icontains=query)
        )

    if sort_by == 'oldest':
        bookings = bookings.order_by('created_at')
    else:
        bookings = bookings.order_by('-created_at')

    paginator = Paginator(bookings, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': site_settings,
        'bookings': page_obj,
        'query': query,
        'sort_by': sort_by,
    }

    return render(request, 'pages/user/cars/index.html', context)

@login_required
def planeBooking(request):
    site_settings = Setting.objects.first()

    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    bookings = PlaneBooking.objects.filter(user=request.user)

    if query:
        bookings = bookings.filter(
            Q(full_name__icontains=query) |
            Q(origin__icontains=query) |
            Q(destination__icontains=query) |
            Q(email__icontains=query)
        )

    if sort_by == 'oldest':
        bookings = bookings.order_by('created_at')
    else:
        bookings = bookings.order_by('-created_at')

    paginator = Paginator(bookings, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add formatted fields for display
    for booking in page_obj:
        booking.pretty_trip_type = booking.trip_type.replace('_', ' ').title()
        booking.pretty_travel_class = booking.travel_class.replace('_', ' ').title()

    context = {
        'settings': site_settings,
        'bookings': page_obj,
        'query': query,
        'sort_by': sort_by,
    }

    return render(request, 'pages/user/planes/index.html', context)

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
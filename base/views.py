import random
from base.forms import *
from base.models import *
from car.models import *
from random import sample
from hotel.models import *
from django.conf import settings
from django.contrib import messages
from django.db.models import Avg, Q
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

def home(request):
    site_settings = Setting.objects.first()

    # 1. Car Brands
    car_brands = list(CarBrand.objects.all())
    car_brands = random.sample(car_brands, min(6, len(car_brands)))

    # 2. Hotels: based on rating or fallback to stars
    rated_hotels = Hotel.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__isnull=False)
    if rated_hotels.exists():
        hotels = rated_hotels.order_by('-avg_rating')[:12]
    else:
        hotels = Hotel.objects.order_by('-stars')[:12]

    hotels = sample(list(hotels), min(6, len(hotels)))  # Random 6 from selected

    # 3. Hotel Rooms: rated first, fallback to random-named to reach total of 6
    rated_rooms = list(
        HotelRoom.objects.annotate(avg_rating=Avg('reviews__rating'))
        .filter(avg_rating__isnull=False)
        .order_by('-avg_rating')[:6]
    )

    # If less than 6, get additional rooms by name ordering and randomize
    if len(rated_rooms) < 6:
        exclude_ids = [room.id for room in rated_rooms]
        fillers = list(
            HotelRoom.objects.exclude(id__in=exclude_ids)
            .order_by('?')[:6 - len(rated_rooms)]
        )
        rooms = rated_rooms + fillers
    else:
        rooms = rated_rooms

    # 4. Best Hotel Rooms: based on highest price
    best_rooms = list(
        HotelRoom.objects.filter(is_available=True)
        .order_by('-price_per_night')[:6]
    )

    # 5. Cars: high-rated or fallback to price
    rated_cars_qs = Car.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__isnull=False)
    rated_cars = list(rated_cars_qs.order_by('-avg_rating')[:6])

    # If less than 6, fill the rest with highest-priced unrated or not-yet-selected cars
    if len(rated_cars) < 6:
        exclude_ids = [car.id for car in rated_cars]
        filler_cars = Car.objects.exclude(id__in=exclude_ids).order_by('-price_per_day')[:6 - len(rated_cars)]
        cars = rated_cars + list(filler_cars)
    else:
        cars = rated_cars

    context = {
        'settings': site_settings,
        'car_brands': car_brands,
        'hotels': hotels,
        'rooms': rooms,
        'best_rooms': best_rooms,
        'cars': cars,
    }

    return render(request, 'pages/index.html', context)

def brands(request):
    site_settings = Setting.objects.first()

    # Query params
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    # Base queryset
    brands = CarBrand.objects.all()

    # Filter by search
    if query:
        brands = brands.filter(Q(name__icontains=query))

    # Sorting
    if sort_by == 'oldest':
        brands = brands.order_by('id')
    else:
        brands = brands.order_by('-id')

    # Pagination
    paginator = Paginator(brands, 12)  # 12 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': site_settings,
        'brands': page_obj,
        'query': query,
        'sort_by': sort_by,
    }

    return render(request, 'pages/brands.html', context)

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
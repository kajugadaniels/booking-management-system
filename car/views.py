from car.models import *
from base.models import *
from django.shortcuts import render
from django.core.paginator import Paginator

def getCars(request):
    site_settings = Setting.objects.first()
    sort_option = request.GET.get('sort', 'latest')

    car_queryset = Car.objects.filter(is_available=True)

    if sort_option == 'price_low_high':
        car_queryset = car_queryset.order_by('price_per_day')
    elif sort_option == 'price_high_low':
        car_queryset = car_queryset.order_by('-price_per_day')
    else:
        car_queryset = car_queryset.order_by('-created_at')  # default: latest

    paginator = Paginator(car_queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': site_settings,
        'cars': page_obj,
        'sort': sort_option,
    }

    return render(request, 'pages/cars/index.html', context)

def carDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/cars/show.html', context)
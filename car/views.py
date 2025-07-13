from car.models import *
from base.models import *
from django.shortcuts import render
from django.core.paginator import Paginator

def getCars(request):
    site_settings = Setting.objects.first()
    sort = request.GET.get('sort')

    cars = Car.objects.filter(is_available=True)

    if sort == 'price_asc':
        cars = cars.order_by('price_per_day')
    elif sort == 'price_desc':
        cars = cars.order_by('-price_per_day')
    else:
        cars = cars.order_by('-created_at')

    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)

    context = {
        'settings': site_settings,
        'cars': cars_page,
        'sort': sort,
    }

    return render(request, 'pages/cars/index.html', context)

def carDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/cars/show.html', context)
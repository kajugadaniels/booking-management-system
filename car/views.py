from car.models import *
from base.models import *
from django.shortcuts import render
from django.core.paginator import Paginator

def getCars(request):
    site_settings = Setting.objects.first()
    cars = Car.objects.filter(is_available=True)

    # === Filters ===
    brand = request.GET.get('car_brand')
    car_type = request.GET.get('car_type')
    condition = request.GET.get('condition')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')
    color = request.GET.get('color')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    features = request.GET.getlist('features')

    # Apply filters
    if brand:
        cars = cars.filter(car_brand_id=brand)

    if car_type:
        cars = cars.filter(car_type_id=car_type)

    if condition:
        cars = cars.filter(condition=condition)

    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)

    if transmission:
        cars = cars.filter(transmission=transmission)

    if color:
        cars = cars.filter(color=color)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)

    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)

    if features:
        cars = cars.filter(carfeature__feature_id__in=features).distinct()

    # === Sorting ===
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        cars = cars.order_by('price_per_day')
    elif sort == 'price_desc':
        cars = cars.order_by('-price_per_day')
    else:
        cars = cars.order_by('-created_at')

    # === Pagination ===
    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)

    context = {
        'settings': site_settings,
        'cars': cars_page,
        'sort': sort,

        # Required for filter form
        'car_brands': CarBrand.objects.all(),
        'car_types': CarType.objects.all(),
        'car_color_choices': dict(Car.COLOR_CHOICES),
        'car_features': Feature.objects.all(),
        'selected_features': list(map(int, features)) if features else [],
    }

    return render(request, 'pages/cars/index.html', context)

def carDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/cars/show.html', context)
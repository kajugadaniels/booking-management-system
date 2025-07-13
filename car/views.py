from car.models import *
from base.models import *
from django.shortcuts import render
from django.core.paginator import Paginator

def getCars(request):
    site_settings = Setting.objects.first()
    cars = Car.objects.filter(is_available=True)

    # === Retrieve filters ===
    sort = request.GET.get('sort')
    location = request.GET.get('location')
    zip_code = request.GET.get('zip_code')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    mileage = request.GET.get('mileage')
    doors = request.GET.get('doors')
    cylinders = request.GET.get('cylinders')
    drive_type = request.GET.get('drive_type')
    fuel_types = request.GET.getlist('fuel_type')
    transmissions = request.GET.getlist('transmission')
    body_types = request.GET.getlist('body_type')
    makes = request.GET.getlist('make')
    models = request.GET.getlist('model')
    features = request.GET.getlist('features')

    # === Apply filters ===
    if location:
        cars = cars.filter(location__iexact=location)

    if zip_code:
        cars = cars.filter(zip_code__iexact=zip_code)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)

    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)

    if mileage:
        cars = cars.filter(mileage__lte=mileage)

    if doors:
        cars = cars.filter(doors=doors)

    if cylinders:
        cars = cars.filter(cylinders=cylinders)

    if drive_type:
        cars = cars.filter(drive_type__iexact=drive_type)

    if fuel_types:
        cars = cars.filter(fuel_type__in=fuel_types)

    if transmissions:
        cars = cars.filter(transmission__in=transmissions)

    if body_types:
        cars = cars.filter(body_type__in=body_types)

    if makes:
        cars = cars.filter(make__in=makes)

    if models:
        cars = cars.filter(model__in=models)

    if features:
        for feature in features:
            cars = cars.filter(features__id=feature)

    # === Sorting ===
    if sort == 'price_asc':
        cars = cars.order_by('price_per_day')
    elif sort == 'price_desc':
        cars = cars.order_by('-price_per_day')
    else:
        cars = cars.order_by('-created_at')

    # === Pagination ===
    paginator = Paginator(cars.distinct(), 9)
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)

    # === Context ===
    context = {
        'settings': site_settings,
        'cars': cars_page,
        'sort': sort,
        'filter_params': request.GET,  # Pass GET for UI re-fill if needed
    }

    return render(request, 'pages/cars/index.html', context)

def carDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/cars/show.html', context)
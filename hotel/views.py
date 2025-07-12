from base.models import *
from hotel.models import *
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator

def getHotels(request):
    site_settings = Setting.objects.first()

    province_filter = request.GET.get('province')
    stars_filter = request.GET.get('stars')
    page_number = request.GET.get('page', 1)

    hotels = Hotel.objects.filter(is_active=True)

    if province_filter:
        hotels = hotels.filter(province__iexact=province_filter)

    if stars_filter:
        try:
            stars = int(stars_filter)
            hotels = hotels.filter(stars=stars)
        except ValueError:
            pass

    hotels = hotels.order_by('-created_at')

    # Attach default image if none exists
    hotel_list = []
    for hotel in hotels:
        image = hotel.images.first()
        hotel_list.append({
            'hotel': hotel,
            'image': image.image.url if image else "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVQfxEyRp184pVTen_MQe-LEqhLZxhWAWj9A&s"
        })

    paginator = Paginator(hotel_list, 12)  # 12 hotels per page
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': site_settings,
        'page_obj': page_obj,
        'selected_province': province_filter,
        'selected_stars': stars_filter,
        'provinces': Hotel.objects.values_list('province', flat=True).distinct(),
        'stars_options': [1, 2, 3, 4, 5]
    }

    return render(request, 'pages/hotels/index.html', context)

def hotelRooms(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/hotels/rooms/index.html', context)

def roomDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/hotels/rooms/show.html', context)
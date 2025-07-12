from base.models import *
from hotel.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

DEFAULT_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVQfxEyRp184pVTen_MQe-LEqhLZxhWAWj9A&s"

def getHotels(request):
    site_settings = Setting.objects.first()
    province_filter = request.GET.get('province')
    stars_filter = request.GET.get('stars')

    hotels = Hotel.objects.all()

    if province_filter:
        hotels = hotels.filter(province__iexact=province_filter)

    if stars_filter:
        try:
            stars_filter = int(stars_filter)
            hotels = hotels.filter(stars=stars_filter)
        except ValueError:
            pass

    hotels = hotels.order_by('-created_at')
    paginator = Paginator(hotels, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    hotel_data = []
    for hotel in page_obj:
        image = HotelImage.objects.filter(hotel=hotel).first()
        image_url = image.image.url if image else DEFAULT_IMAGE
        all_rooms = HotelRoom.objects.filter(hotel=hotel)
        available_rooms = all_rooms.filter(is_available=True)
        hotel_data.append({
            'instance': hotel,
            'image': image_url,
            'room_count': all_rooms.count(),
            'available_rooms': available_rooms.count()
        })

    provinces = Hotel.objects.values_list('province', flat=True).distinct()
    stars = Hotel.objects.values_list('stars', flat=True).distinct().order_by()

    # Clean querystring: remove any duplicate 'page' key
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    cleaned_querystring = get_params.urlencode()

    context = {
        'settings': site_settings,
        'page_obj': page_obj,
        'hotel_data': hotel_data,
        'provinces': provinces,
        'stars': stars,
        'current_province': province_filter,
        'current_stars': stars_filter,
        'cleaned_querystring': cleaned_querystring,
    }

    return render(request, 'pages/hotels/index.html', context)

def hotelRooms(request, hotel_id):
    site_settings = Setting.objects.first()
    hotel = get_object_or_404(Hotel, id=hotel_id)

    rooms = HotelRoom.objects.filter(hotel=hotel).order_by('-created_at')
    paginator = Paginator(rooms, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    cleaned_querystring = get_params.urlencode()

    context = {
        'settings': site_settings,
        'hotel': hotel,
        'page_obj': page_obj,
        'cleaned_querystring': cleaned_querystring
    }

    return render(request, 'pages/hotels/rooms/index.html', context)

def roomDetails(request):
    site_settings = Setting.objects.first()

    context = {
        'settings': site_settings
    }

    return render (request, 'pages/hotels/rooms/show.html', context)
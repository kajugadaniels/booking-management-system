from random import sample
from base.models import *
from hotel.models import *
from django.db.models import Avg
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

    # Build enhanced room data list
    room_data = []
    for room in page_obj:
        # Try getting a valid image
        room_images = RoomImage.objects.filter(room=room)
        image_url = DEFAULT_IMAGE
        for img in room_images:
            try:
                if img.image and hasattr(img.image, 'url'):
                    image_url = img.image.url
                    break
            except:
                continue

        # Get 3 random amenities
        amenities = list(RoomAmenity.objects.filter(room=room).select_related('amenity'))
        random_amenities = sample(amenities, min(3, len(amenities)))

        room_data.append({
            'instance': room,
            'image_url': image_url,
            'amenities': [ra.amenity.name for ra in random_amenities]
        })

    # Clean querystring for pagination
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    cleaned_querystring = get_params.urlencode()

    context = {
        'settings': site_settings,
        'hotel': hotel,
        'page_obj': page_obj,
        'room_data': room_data,
        'cleaned_querystring': cleaned_querystring
    }

    return render(request, 'pages/hotels/rooms/index.html', context)

def roomDetails(request, hotel_id, room_id):
    site_settings = Setting.objects.first()
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = get_object_or_404(HotelRoom, id=room_id, hotel=hotel)

    images = RoomImage.objects.filter(room=room)
    amenities = RoomAmenity.objects.filter(room=room).select_related('amenity')
    reviews = RoomReview.objects.filter(room=room).select_related('user')
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    similar_rooms = HotelRoom.objects.filter(hotel=hotel).exclude(id=room.id)[:4]

    context = {
        'settings': site_settings,
        'hotel': hotel,
        'room': room,
        'images': images,
        'amenities': amenities,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'similar_rooms': similar_rooms,
    }

    return render(request, 'pages/hotels/rooms/show.html', context)
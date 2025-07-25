import uuid
from random import sample
from base.models import *
from hotel.forms import *
from hotel.models import *
from payment.utils import *
from payment.models import *
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

DEFAULT_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVQfxEyRp184pVTen_MQe-LEqhLZxhWAWj9A&s"

def getHotels(request):
    site_settings = Setting.objects.first()

    # --- Get filters from query string
    province_filter = request.GET.get('province')
    stars_filter = request.GET.get('stars')
    review_sort = request.GET.get('review_sort')

    # --- Base queryset
    hotels = Hotel.objects.annotate(avg_rating=Avg('reviews__rating'))

    # --- Apply filters
    if province_filter:
        hotels = hotels.filter(province__iexact=province_filter)

    if stars_filter:
        try:
            stars_filter = int(stars_filter)
            hotels = hotels.filter(stars=stars_filter)
        except ValueError:
            pass

    # --- Apply sorting
    if review_sort == 'high':
        hotels = hotels.order_by('-avg_rating', '-created_at')
    elif review_sort == 'low':
        hotels = hotels.order_by('avg_rating', '-created_at')
    else:
        hotels = hotels.order_by('-created_at')

    # --- Pagination
    paginator = Paginator(hotels, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- Prepare data for template
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
            'available_rooms': available_rooms.count(),
            'avg_rating': round(hotel.avg_rating or 0, 1),
        })

    # --- For filters
    provinces = [label for _, label in Hotel.PROVINCE_CHOICES]
    stars = Hotel.objects.values_list('stars', flat=True).distinct().order_by()

    # --- Clean querystring for pagination links
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
        'review_sort': review_sort,
        'cleaned_querystring': cleaned_querystring,
    }

    return render(request, 'pages/hotels/index.html', context)

def hotelRooms(request, hotel_id):
    site_settings = Setting.objects.first()
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = HotelRoom.objects.filter(hotel=hotel, is_available=True)

    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    occupancy = request.GET.get('occupancy')
    room_type = request.GET.get('room_type')
    bed_type = request.GET.get('bed_type')
    refundable = request.GET.get('refundable')
    selected_amenities = request.GET.getlist('amenities')

    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)
    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)
    if occupancy:
        rooms = rooms.filter(occupancy=occupancy)
    if room_type:
        rooms = rooms.filter(room_type__iexact=room_type)
    if bed_type:
        rooms = rooms.filter(bed_type__iexact=bed_type)
    if refundable in ['true', 'false']:
        rooms = rooms.filter(refundable=(refundable == 'true'))
    if selected_amenities:
        for amenity_id in selected_amenities:
            rooms = rooms.filter(room_amenities__amenity_id=amenity_id)

    # Sorting
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        rooms = rooms.order_by('price_per_night')
    elif sort == 'price_desc':
        rooms = rooms.order_by('-price_per_night')
    else:
        rooms = rooms.order_by('-created_at')

    # Pagination
    paginator = Paginator(rooms.distinct(), 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Image & amenities processing
    room_data = []
    for room in page_obj:
        image_url = DEFAULT_IMAGE
        for img in RoomImage.objects.filter(room=room):
            try:
                if img.image and hasattr(img.image, 'url'):
                    image_url = img.image.url
                    break
            except:
                continue

        amenities = list(RoomAmenity.objects.filter(room=room).select_related('amenity'))
        random_amenities = sample(amenities, min(3, len(amenities)))

        room_data.append({
            'instance': room,
            'image_url': image_url,
            'amenities': [ra.amenity.name for ra in random_amenities],
        })

    # Query string for clean pagination links
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    cleaned_querystring = get_params.urlencode()

    context = {
        'settings': site_settings,
        'hotel': hotel,
        'page_obj': page_obj,
        'room_data': room_data,
        'room_types': HotelRoom.ROOM_TYPE_CHOICES,
        'bed_types': HotelRoom.BED_TYPE_CHOICES,
        'amenities': Amenity.objects.all(),
        'selected_amenities': [int(a) for a in selected_amenities],
        'sort': sort,
        'cleaned_querystring': cleaned_querystring,
    }

    return render(request, 'pages/hotels/rooms/index.html', context)

def roomDetails(request, hotel_id, room_id):
    site_settings = Setting.objects.first()
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = get_object_or_404(HotelRoom, id=room_id, hotel=hotel)
    images = room.images.all()
    amenities = room.room_amenities.select_related('amenity')
    reviews = RoomReview.objects.filter(room=room).select_related('user')
    similar_rooms = HotelRoom.objects.filter(hotel=hotel).exclude(id=room.id)[:7]
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    review_form = None
    booking_form = None
    invoice_number = None  # ✅ Will be set via session or after booking

    # ✅ Retrieve invoice from session (set after redirect)
    invoice_number = request.session.pop('recent_invoice', None)

    # --- Handle review submission ---
    if request.user.is_authenticated:
        if request.method == 'POST' and 'book_room' not in request.POST:
            review_form = RoomReviewForm(request.POST)
            if review_form.is_valid():
                if RoomReview.objects.filter(user=request.user, room=room).exists():
                    messages.warning(request, "You have already submitted a review for this room.")
                else:
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.room = room
                    try:
                        review.save()

                        subject = 'Thank You for Your Review!'
                        message = render_to_string('emails/review_thanks.html', {
                            'user': request.user,
                            'room': room,
                            'settings': site_settings
                        })
                        send_mail(subject, '', settings.EMAIL_HOST_USER, [request.user.email], html_message=message)

                        messages.success(request, 'Your review has been submitted. Thank you!')
                        return redirect('hotel:roomDetails', hotel_id=hotel.id, room_id=room.id)
                    except IntegrityError:
                        messages.error(request, "You have already submitted a review for this room.")
        else:
            review_form = RoomReviewForm()

    # --- Handle booking form ---
    if request.user.is_authenticated:
        if request.method == 'POST' and 'book_room' in request.POST:
            booking_form = RoomBookingForm(request.POST)
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.room = room
                booking.status = 'pending'

                nights = (booking.check_out - booking.check_in).days
                booking.total_price = nights * room.price_per_night
                booking.save()

                # --- Extract user contact info ---
                customer_email = request.user.email
                customer_name = getattr(request.user, 'name', None) or request.user.username
                customer_phone = getattr(request.user, 'phone_number', '0780000001')  # fallback if not defined

                # --- Generate a temporary transaction ID
                transaction_id = str(uuid.uuid4())
                callback_url = f"https://plutobooking.com/callback/{transaction_id}"

                # --- Register invoice with IremboPay ---
                status_code, irembo_invoice_number = createInvoiceOnIremboPay(
                    invoiceNumber=transaction_id,
                    amount=booking.total_price,
                    description=f"Room booking for {customer_name} at {booking.room.hotel.name}",
                    callbackUrl=callback_url,
                    customerEmail=customer_email,
                    customerName=customer_name,
                    customerPhone=customer_phone
                )

                if status_code != 201 or not irembo_invoice_number:
                    messages.error(request, "Failed to register invoice with payment gateway.")
                    return redirect('hotel:roomDetails', hotel_id=hotel.id, room_id=room.id)

                # ✅ Save correct invoice number string
                RoomPayment.objects.create(
                    booking=booking,
                    invoice_number=irembo_invoice_number,
                    status='pending'
                )

                # Save for use on redirect
                request.session['recent_invoice'] = irembo_invoice_number

                # --- Send emails ---
                user_subject = "Your Room Booking Has Been Received"
                user_message = render_to_string('emails/user_booking_confirmation.html', {
                    'user': request.user,
                    'booking': booking,
                    'room': room,
                    'hotel': hotel,
                    'settings': site_settings
                })
                send_mail(user_subject, '', settings.EMAIL_HOST_USER, [customer_email], html_message=user_message)

                admin_subject = "New Room Booking Received"
                admin_message = render_to_string('emails/admin_booking_notification.html', {
                    'booking': booking,
                    'user': request.user,
                    'room': room,
                    'hotel': hotel,
                    'settings': site_settings
                })
                send_mail(admin_subject, '', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message=admin_message)

                messages.success(request, f"Booking confirmed for {nights} night(s)! Proceed to payment.")
                return redirect('payment:payRoomBooking', invoice_number=irembo_invoice_number)
        else:
            booking_form = RoomBookingForm()

    # --- Final context ---
    context = {
        'settings': site_settings,
        'room': room,
        'hotel': hotel,
        'images': images,
        'amenities': amenities,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'similar_rooms': similar_rooms,
        'review_form': review_form,
        'booking_form': booking_form,
        'invoice_number': invoice_number,  # ✅ now always set properly
    }

    return render(request, 'pages/hotels/rooms/show.html', context)
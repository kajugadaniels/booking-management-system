import uuid
from car.forms import *
from car.models import *
from base.models import *
from payment.utils import *
from payment.models import *
from django.db.models import Avg
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect

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

def carDetails(request, id):
    site_settings = Setting.objects.first()
    car = get_object_or_404(Car, id=id)

    images = car.images.all()
    features = Feature.objects.filter(carfeature__car=car)
    reviews = car.reviews.select_related('user').all()
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    car_brand = car.car_brand
    similar_cars = Car.objects.filter(car_brand=car_brand, is_available=True).exclude(id=car.id)[:7]

    review_form = None
    booking_form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            review_form = CarReviewForm(request.POST)
            if review_form.is_valid():
                # Check if user has already submitted a review for this car
                if CarReview.objects.filter(user=request.user, car=car).exists():
                    messages.warning(request, "You have already submitted a review for this car.")
                else:
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.car = car
                    try:
                        review.save()
                        # Send thank-you email
                        subject = 'Thank You for Your Review!'
                        message = render_to_string('emails/car_review_thanks.html', {
                            'user': request.user,
                            'car': car,
                            'settings': site_settings
                        })
                        send_mail(subject, '', settings.EMAIL_HOST_USER, [request.user.email], html_message=message)

                        messages.success(request, 'Your review has been submitted. Thank you!')
                        return redirect('car:carDetails', id=car.id)
                    except IntegrityError:
                        messages.error(request, "You have already submitted a review for this car.")
        else:
            review_form = CarReviewForm()

    # Booking logic
    if request.user.is_authenticated:
        if request.method == 'POST' and 'book_car' in request.POST:
            booking_form = CarBookingForm(request.POST)
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.car = car
                booking.status = 'pending'

                days = (booking.dropoff_date - booking.pickup_date).days
                booking.total_price = days * car.price_per_day
                booking.save()

                # Create Irembo Invoice
                customer_email = request.user.email
                customer_name = getattr(request.user, 'name', None) or request.user.username
                customer_phone = getattr(request.user, 'phone_number', '0780000001')
                transaction_id = str(uuid.uuid4())
                callback_url = f"https://plutobooking.com/callback/{transaction_id}"

                status_code, irembo_invoice_number = createInvoiceOnIremboPay(
                    invoiceNumber=transaction_id,
                    amount=booking.total_price,
                    description=f"Car booking for {customer_name} ({booking.car.name})",
                    callbackUrl=callback_url,
                    customerEmail=customer_email,
                    customerName=customer_name,
                    customerPhone=customer_phone
                )

                if status_code != 201 or not irembo_invoice_number:
                    messages.error(request, "Failed to initiate payment.")
                    return redirect('car:carDetails', id=car.id)

                CarPayment.objects.create(
                    booking=booking,
                    invoice_number=irembo_invoice_number,
                    status='pending'
                )

                request.session['recent_invoice'] = irembo_invoice_number

                # Emails
                user_subject = "Your Car Booking Has Been Received"
                user_message = render_to_string('emails/user_car_booking_confirmation.html', {
                    'user': request.user,
                    'booking': booking,
                    'car': car,
                    'settings': site_settings
                })
                send_mail(user_subject, '', settings.EMAIL_HOST_USER, [customer_email], html_message=user_message)

                admin_subject = "New Car Booking Received"
                admin_message = render_to_string('emails/admin_car_booking_notification.html', {
                    'booking': booking,
                    'user': request.user,
                    'car': car,
                    'settings': site_settings
                })
                send_mail(admin_subject, '', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message=admin_message)

                messages.success(request, f"Booking confirmed for {days} day(s)! Proceed to payment.")
                return redirect('payment:payCarBooking', invoice_number=irembo_invoice_number)
        else:
            booking_form = CarBookingForm()

    context = {
        'settings': site_settings,
        'car': car,
        'images': images,
        'features': features,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'similar_cars': similar_cars,
        'review_form': review_form,
        'booking_form': booking_form,
    }

    return render(request, 'pages/cars/show.html', context)
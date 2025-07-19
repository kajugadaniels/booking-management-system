import os
from dotenv import load_dotenv
from payment.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

load_dotenv()

@login_required
def payRoomBooking(request, invoice_number):
    payment = get_object_or_404(RoomPayment, invoice_number=invoice_number)

    # Ensure the logged-in user owns the booking
    if payment.booking.user != request.user:
        return redirect('base:home')

    # Only allow payment if still pending
    if payment.status != 'pending':
        return redirect('hotel:roomDetails', hotel_id=payment.booking.room.hotel.id, room_id=payment.booking.room.id)

    context = {
        'payment': payment,
        'public_key': os.getenv("IREMBO_PUBLIC_KEY"),
    }
    return render(request, 'pages/payment/room_payment.html', context)

@login_required
def payCarBooking(request, invoice_number):
    payment = get_object_or_404(CarPayment, invoice_number=invoice_number)

    # Ensure the logged-in user owns the booking
    if payment.booking.user != request.user:
        return redirect('base:home')

    # Prevent duplicate payments
    if payment.status != 'pending':
        return redirect('car:carDetails', id=payment.booking.car.id)

    context = {
        'payment': payment,
        'public_key': os.getenv("IREMBO_PUBLIC_KEY"),
    }
    return render(request, 'pages/payment/car_payment.html', context)
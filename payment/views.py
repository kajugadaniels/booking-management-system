from payment.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect


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
        'public_key': "pk_live_a780e931399b42f6a135dd09e897ec32",
    }
    return render(request, 'pages/payment/room_payment.html', context)

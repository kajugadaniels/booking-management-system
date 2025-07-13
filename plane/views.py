from base.models import *
from plane.forms import *
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

def getPlanes(request):
    site_settings = Setting.objects.first()
    form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PlaneBookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()

                # Email to user
                user_subject = "Your Plane Booking Request Received"
                user_message = render_to_string('emails/plane_user_confirmation.html', {
                    'user': request.user,
                    'booking': booking,
                    'settings': site_settings,
                })
                send_mail(user_subject, '', settings.EMAIL_HOST_USER, [request.user.email], html_message=user_message)

                # Email to admin
                admin_subject = "New Plane Booking Request"
                admin_message = render_to_string('emails/plane_admin_notification.html', {
                    'booking': booking,
                    'user': request.user,
                    'settings': site_settings,
                })
                send_mail(admin_subject, '', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message=admin_message)

                messages.success(request, "Your flight booking request has been submitted.")
                return redirect('plane:getPlanes')
        else:
            form = PlaneBookingForm()

    context = {
        'settings': site_settings,
        'form': form,
    }

    return render(request, 'pages/planes/index.html', context)

from django.db import models
from django.conf import settings
from django.utils import timezone

class PlaneBooking(models.Model):
    TRAVEL_CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('premium_economy', 'Premium Economy'),
        ('business', 'Business'),
        ('first_class', 'First Class'),
    ]

    TRIP_TYPE_CHOICES = [
        ('one_way', 'One Way'),
        ('round_trip', 'Round Trip'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plane_bookings')

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)

    origin = models.CharField(max_length=255, help_text="City or Airport of Departure")
    destination = models.CharField(max_length=255, help_text="City or Airport of Arrival")

    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES, default='one_way')
    travel_class = models.CharField(max_length=20, choices=TRAVEL_CLASS_CHOICES, default='economy')

    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    num_infants = models.PositiveIntegerField(default=0)

    notes = models.TextField(blank=True, help_text="Any special requests or additional info")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.origin} to {self.destination}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Plane Booking"
        verbose_name_plural = "Plane Bookings"

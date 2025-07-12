import os
import random
from account.models import *
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField

def hotel_image_upload_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'hotels/hotel_{slugify(instance.hotel.name)}_{timezone.now().strftime("%Y%m%d%H%M%S")}{file_extension}'

class Hotel(models.Model):
    STAR_CHOICES = [(i, f'{i} Star') for i in range(1, 6)]

    name = models.CharField(max_length=255)
    description = models.TextField()
    stars = models.IntegerField(choices=STAR_CHOICES)
    address = models.CharField(max_length=255)
    map_url = models.URLField(blank=True, null=True)

    # Location fields
    country = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    cell = models.CharField(max_length=100)
    village = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(
        upload_to=hotel_image_upload_path,
        processors=[ResizeToFill(1280, 720)],
        format='JPEG',
        options={'quality': 90},
    )
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image of {self.hotel.name}"

class HotelReview(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel_reviews')

    rating = models.PositiveSmallIntegerField(choices=[(i, f'{i} Star') for i in range(1, 6)])
    title = models.CharField(max_length=255)
    review = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.hotel.name} ({self.rating}★)"

    class Meta:
        unique_together = ('hotel', 'user')
        ordering = ['-created_at']

def room_image_upload_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'hotel-rooms/room_{slugify(instance.room.hotel.name)}_{slugify(instance.room.name)}_{timezone.now().strftime("%Y%m%d%H%M%S")}{file_extension}'

class HotelRoom(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='rooms')

    name = models.CharField(max_length=255)
    room_type = models.CharField(max_length=100)  # e.g. Deluxe King, Suite
    description = models.TextField()
    bed_type = models.CharField(max_length=100, help_text="e.g. 1 King Bed or 2 Twin Beds")
    occupancy = models.PositiveIntegerField(help_text="Maximum number of guests")
    size = models.CharField(max_length=50, help_text="e.g. 30 sqm")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    refundable = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

    class Meta:
        ordering = ['-created_at']

class RoomImage(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(
        upload_to=room_image_upload_path,
        processors=[ResizeToFill(1280, 720)],
        format='JPEG',
        options={'quality': 90},
    )
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.room.name}"

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Optional CSS class or icon path")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RoomAmenity(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='room_amenities')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room', 'amenity')

    def __str__(self):
        return f"{self.room.name} - {self.amenity.name}"

class RoomReview(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(choices=[(i, f'{i} Star') for i in range(1, 6)])
    title = models.CharField(max_length=255)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.room.name} ({self.rating}★)"

    class Meta:
        unique_together = ('room', 'user')
        ordering = ['-created_at']
import os
import random
from account.models import *
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.db.models.signals import post_delete, pre_save

def hotel_image_upload_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'hotels/hotel_{slugify(instance.hotel.name)}_{timezone.now().strftime("%Y%m%d%H%M%S")}{file_extension}'

class Hotel(models.Model):
    STAR_CHOICES = [(i, f'{i} Star') for i in range(1, 6)]

    name = models.CharField(max_length=255)
    description = models.TextField()
    stars = models.IntegerField(choices=STAR_CHOICES)
    address = models.CharField(max_length=255)
    map_url = models.TextField(blank=True, null=True)

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
    ROOM_TYPE_CHOICES = [
        ("single", "Single Room"),
        ("double", "Double Room"),
        ("twin", "Twin Room"),
        ("triple", "Triple Room"),
        ("quad", "Quad Room"),
        ("queen", "Queen Room"),
        ("king", "King Room"),
        ("standard", "Standard Room"),
        ("deluxe", "Deluxe Room"),
        ("superior", "Superior Room"),
        ("executive", "Executive Room"),
        ("junior_suite", "Junior Suite"),
        ("suite", "Suite"),
        ("penthouse", "Penthouse Suite"),
        ("family", "Family Room"),
        ("accessible", "Accessible Room"),
        ("studio", "Studio"),
        ("connecting", "Connecting Rooms"),
        ("presidential", "Presidential Suite"),
        ("executive_suite", "Executive Suite"),
    ]

    BED_TYPE_CHOICES = [
        ("king", "King Bed"),
        ("queen", "Queen Bed"),
        ("twin", "Twin Beds"),
        ("double", "Double Bed"),
    ]

    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='rooms')

    name = models.CharField(max_length=255)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    description = models.TextField()
    bed_type = models.CharField(max_length=50, choices=BED_TYPE_CHOICES)
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
    room = models.ForeignKey('HotelRoom', on_delete=models.CASCADE, related_name='images')
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

# ✅ Delete image file when RoomImage is deleted
@receiver(post_delete, sender=RoomImage)
def delete_room_image_file(sender, instance, **kwargs):
    if instance.image and instance.image.storage.exists(instance.image.name):
        instance.image.delete(save=False)

# ✅ Delete old file when RoomImage is updated with a new image
@receiver(pre_save, sender=RoomImage)
def auto_delete_old_room_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, no image to replace

    try:
        old_instance = RoomImage.objects.get(pk=instance.pk)
    except RoomImage.DoesNotExist:
        return

    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image:
        if old_image.storage.exists(old_image.name):
            old_image.delete(save=False)

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

class RoomBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_bookings')
    room = models.ForeignKey('HotelRoom', on_delete=models.CASCADE, related_name='bookings')
    
    check_in = models.DateField()
    check_out = models.DateField()

    guests = models.PositiveSmallIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def duration(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return f"{self.user.name} - {self.room.name} from {self.check_in} to {self.check_out}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Room Booking"
        verbose_name_plural = "Room Bookings"
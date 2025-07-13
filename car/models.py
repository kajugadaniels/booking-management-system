import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.db.models.signals import post_delete
from django.db.models.signals import post_delete, pre_save
from django.core.validators import MinValueValidator, MaxValueValidator

def car_image_upload_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"cars/car_{slugify(instance.car.name)}_{timestamp}{file_extension}"

def brand_thumbnail_upload_path(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"brands/{instance.name.lower().replace(' ', '_')}_thumb{ext}"

class CarType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car Type"
        verbose_name_plural = "Car Types"

class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"

class CarBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    thumbnail = ProcessedImageField(
        upload_to=brand_thumbnail_upload_path,
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car Brand"
        verbose_name_plural = "Car Brands"

# ✅ Delete thumbnail file when CarBrand is deleted
@receiver(post_delete, sender=CarBrand)
def delete_car_brand_thumbnail(sender, instance, **kwargs):
    if instance.thumbnail and instance.thumbnail.storage.exists(instance.thumbnail.name):
        instance.thumbnail.delete(save=False)

# ✅ Delete old thumbnail file when CarBrand thumbnail is updated
@receiver(pre_save, sender=CarBrand)
def auto_delete_old_car_brand_thumbnail_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New brand, no previous image

    try:
        old_instance = CarBrand.objects.get(pk=instance.pk)
    except CarBrand.DoesNotExist:
        return

    old_image = old_instance.thumbnail
    new_image = instance.thumbnail

    if old_image and old_image != new_image:
        if old_image.storage.exists(old_image.name):
            old_image.delete(save=False)

class Car(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    DOORS_CHOICES = [
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('gray', 'Gray'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('silver', 'Silver'),
        ('green', 'Green'),
    ]
    FUEL_TYPES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=255)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.SET_NULL, null=True, blank=True)
    car_type = models.ForeignKey(CarType, on_delete=models.SET_NULL, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    doors = models.IntegerField(choices=DOORS_CHOICES)
    year = models.PositiveIntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    body = models.CharField(max_length=100)
    engine_capacity = models.DecimalField(max_digits=5, decimal_places=2, help_text="In Liters")
    mileage = models.PositiveIntegerField(help_text="In kilometers")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(
        upload_to=car_image_upload_path,
        processors=[ResizeToFill(1280, 720)],
        format='JPEG',
        options={'quality': 90},
    )
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image of {self.car.name}"

# Delete image file from media folder when model is deleted
@receiver(post_delete, sender=CarImage)
def delete_car_image_file(sender, instance, **kwargs):
    if instance.image and instance.image.storage.exists(instance.image.name):
        instance.image.delete(save=False)

class CarFeature(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('car', 'feature')
        verbose_name = "Car Feature"
        verbose_name_plural = "Car Features"

    def __str__(self):
        return f"{self.car.name} - {self.feature.name}"

class CarReview(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('car', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} - {self.car.name} ({self.rating}★)"

class CarBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_bookings')

    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    dropoff_date = models.DateField()

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.car.name} Booking"

    class Meta:
        ordering = ['-created_at']
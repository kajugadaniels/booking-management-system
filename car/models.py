import os
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

def car_image_upload_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"cars/car_{slugify(instance.car.name)}_{timestamp}{file_extension}"


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
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
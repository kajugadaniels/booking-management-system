import os
import random
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from imagekit.models import ProcessedImageField

class Setting(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure only one instance of settings can exist
        if not self.pk and Setting.objects.exists():
            raise ValueError("You can only create one instance of the settings.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Website Settings"

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
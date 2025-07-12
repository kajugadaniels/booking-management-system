import os
import random
from account.models import *
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
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

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
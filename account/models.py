import os
from django.db import models
from account.managers import *
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

def user_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'profile_images/user_{slugify(instance.name)}_{instance.phone_number}{file_extension}'

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    image = ProcessedImageField(
        upload_to=user_image_path,
        processors=[ResizeToFill(720, 720)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # OTP fields for password reset functionality
    reset_otp = models.CharField(max_length=7, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.email if self.email else self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(User, self).save(*args, **kwargs)

# ✅ Delete profile image file when user is deleted
@receiver(post_delete, sender=User)
def delete_user_image_file(sender, instance, **kwargs):
    if instance.image and instance.image.storage.exists(instance.image.name):
        instance.image.delete(save=False)

# ✅ Delete old image file when user updates their profile picture
@receiver(pre_save, sender=User)
def auto_delete_old_user_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New user, no existing image to replace

    try:
        old_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image:
        if old_image.storage.exists(old_image.name):
            old_image.delete(save=False)
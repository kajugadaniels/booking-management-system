from django import forms
from car.models import *
from django.utils import timezone

class CarReviewForm(forms.ModelForm):
    class Meta:
        model = CarReview
        fields = ['rating', 'title', 'review']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Good Car', 'class': 'form-control'}),
            'review': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)], attrs={'class': 'form-control'})
        }

class CarBookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['pickup_location', 'dropoff_location', 'pickup_date', 'dropoff_date']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dropoff_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special needs...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get("pickup_date")
        dropoff_date = cleaned_data.get("dropoff_date")

        if pickup_date and dropoff_date:
            if pickup_date < timezone.now().date():
                self.add_error('pickup_date', "Pickup date cannot be in the past.")
            if dropoff_date <= pickup_date:
                self.add_error('dropoff_date', "Dropoff must be after Pickup.")

        return cleaned_data
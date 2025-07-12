from django import forms
from hotel.models import *
from django.utils import timezone

class RoomReviewForm(forms.ModelForm):
    class Meta:
        model = RoomReview
        fields = ['rating', 'title', 'review']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Good Room', 'class': 'form-control'}),
            'review': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)], attrs={'class': 'form-control'})
        }

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['check_in', 'check_out', 'guests', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special needs...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out:
            if check_in < timezone.now().date():
                self.add_error('check_in', "Check-in date cannot be in the past.")
            if check_out <= check_in:
                self.add_error('check_out', "Check-out must be after check-in.")

        return cleaned_data
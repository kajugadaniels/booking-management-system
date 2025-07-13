from django import forms
from plane.models import *

class PlaneBookingForm(forms.ModelForm):
    class Meta:
        model = PlaneBooking
        exclude = ['user', 'created_at']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'origin': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'travel_class': forms.Select(attrs={'class': 'form-control'}),
            'trip_type': forms.Select(attrs={'class': 'form-control'}),
            'num_adults': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_children': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_infants': forms.NumberInput(attrs={'class': 'form-control'}),
        }

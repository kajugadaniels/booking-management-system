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
from django import forms
from hotel.models import *

class RoomReviewForm(forms.ModelForm):
    class Meta:
        model = RoomReview
        fields = ['rating', 'title', 'review']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Good Room', 'class': 'form-control'}),
            'review': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)], attrs={'class': 'form-control'})
        }
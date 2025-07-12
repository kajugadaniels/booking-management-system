from django import forms
from account.models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if User.objects.exclude(id=user_id).filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        user_id = self.instance.id
        if User.objects.exclude(id=user_id).filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already taken.")
        return phone

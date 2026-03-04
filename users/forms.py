from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow Customer or Hotel Manager registration from public facing form
        self.fields['role'].choices = [
            ('CUSTOMER', 'Customer'),
            ('HOTEL_MANAGER', 'Hotel Manager')
        ]

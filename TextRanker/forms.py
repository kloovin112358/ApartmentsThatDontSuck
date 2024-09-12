# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import *

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = CustomUser.objects.filter(
            email__iexact=email,
            is_active=True,
        )
        return active_users

class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class UnitUpdateForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['status', 'neighborhood', 'unitType', 'listing_link', 'price', 'quality_rating', 'note']

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User  # Import the User model

from myapp.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(label='Age')
    height = forms.DecimalField(max_digits=5, decimal_places=2, label='Height')
    weight = forms.DecimalField(max_digits=5, decimal_places=2, label='Weight')
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User  # Use the User model
        fields = UserCreationForm.Meta.fields + ('age', 'height', 'weight', 'email')


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['height', 'weight', 'age']

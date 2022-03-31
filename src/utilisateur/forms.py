from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import kwgPerson

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class kwgPersonUpdateForm(forms.ModelForm):
    class Meta:
        model = kwgPerson
        fields = ['image', 'roles',]
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import kwgPerson

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2',
                'first_name', 'last_name','groups']

class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','groups']

class kwgPersonUpdateForm(forms.ModelForm):
    class Meta:
        model = kwgPerson
        fields = ['image','roles',]

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegisterForm, UserUpdateForm, kwgPersonUpdateForm
from django.contrib.auth.models import Group

from .models import kwgPerson

class GroupsList(ListView):
    model = Group
    template_name = "utilisateur/groups.html"

class UsersList(ListView):
    model = kwgPerson
    template_name = "utilisateur/users_list.html"

class LogoutView(LogoutView,SuccessMessageMixin):
    template_name = 'utilisateur/logout.html'

class LoginView(SuccessMessageMixin,LoginView):
    template_name = 'utilisateur/login.html'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'utilisateur/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = kwgPersonUpdateForm(request.POST, request.FILES, instance=request.user.personne)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = kwgPersonUpdateForm(instance=request.user.personne)
    context = {'u_form':u_form,'p_form':p_form}
    return render(request, 'utilisateur/profile.html', context)

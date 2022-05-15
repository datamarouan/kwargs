from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegisterForm, UserUpdateForm, kwgPersonUpdateForm
from django.contrib.auth.models import Group, User

from .models import kwgPerson

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

class PasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'utilisateur/password/password_reset.html'
    email_template_name = 'utilisateur/password/password_reset_email.html'
    subject_template_name = 'utilisateur/password/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('profile')

class GroupsDetailView(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Group
    template_name = "utilisateur/crud/group_details.html"

class GroupsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Group
    fields = ["name",]
    template_name = "utilisateur/crud/group_ajout.html"
    success_message = "Le groupe %(name)s a bien été créé."
    success_url = "/groupes/"

class GroupsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Group
    fields = ["name",]
    template_name = "utilisateur/crud/group_ajout.html"
    success_message = "Les modifications au groupe %(name)s ont été enregistrées."
    success_url = "/groupes/"

class GroupsDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Group 
    template_name = "objet_a_effacer.html"
    success_message = "Le groupe %(name)s a été effacé"
    success_url = "/groupes/"

class GroupsList(ListView):
    model = Group
    template_name = "utilisateur/groups.html"

class UsersList(ListView):
    model = kwgPerson
    template_name = "utilisateur/users_list.html"

class LogoutView(SuccessMessageMixin, LogoutView):
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
            messages.success(request, 'Vos informations ont été mises à jour.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = kwgPersonUpdateForm(instance=request.user.personne)
    context = {'u_form':u_form,'p_form':p_form}
    return render(request, 'utilisateur/profile.html', context)

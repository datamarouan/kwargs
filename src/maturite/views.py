from .models import *
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View, TemplateView

def index(request):
	return render(request, "maturite/accueil.html", context)
from .models import *
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View, TemplateView

def index(request):
	projets = Projet.objects.all()
	taches = Tache.objects.all()

	context = {"projets":projets, "taches":taches}
	return render(request, "projet/accueil.html", context)

class ProjetCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Projet
	fields = "__all__"
	template_name = "projet/crud/projet_ajout.html"
	success_message = "Le projet %(nom)s a été créé"

class ProjetUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Projet
	fields = "__all__"
	template_name = "projet/crud/projet_ajout.html"
	success_message = "%(nom)s a bien été modifié"

class ProjetDetailView(LoginRequiredMixin, DetailView):
	model = Projet
	template_name = "projet/crud/projet_details.html"

class ProjetDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Projet
	template_name = "objet_a_effacer.html"
	success_message = "%(nom)s a été effacé. (Que le grand cric me croque)"

class TacheCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Tache
	fields = "__all__"
	template_name = "projet/crud/tache_ajout.html"
	success_message = "La tâche %(nom)s a été créé"

class TacheUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Tache
	fields = "__all__"
	template_name = "projet/crud/tache_ajout.html"
	success_message = "%(nom)s a bien été modifié"

class TacheDetailView(LoginRequiredMixin, DetailView):
	model = Tache
	template_name = "projet/crud/tache_details.html"

class TacheDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Tache
	template_name = "objet_a_effacer.html"
	success_message = "%(nom)s a été effacé. (Que le grand cric me croque)"
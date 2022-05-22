from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from .models import *

@login_required
def index(request):
	taches = Ticket.objects.all()
	context = {"taches":taches}
	return render(request, 'ticket/accueil.html', context)

class TicketDetailView(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "ticket/crud/ticket_details.html"

class TicketCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Ticket
    fields = "__all__"
    template_name = "ticket/crud/ticket_ajout.html"
    success_message = "Le ticket %(titre)s a bien été créé."
    success_url = "/tickets/"

class TicketUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = "__all__"
    template_name = "ticket/crud/ticket_ajout.html"
    success_message = "Les modifications au ticket %(titre)s ont été enregistrées."
    success_url = "/tickets/"

class TicketDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "objet_a_effacer.html"
    success_message = "Le ticket %(titre)s a été effacé"
    success_url = "/tickets/"

class TicketAFaire(LoginRequiredMixin, ListView):
    queryset = Ticket.objects.all().filter(status="A faire")
    template_name = "ticket/vues/a_faire.html"

class TicketFait(LoginRequiredMixin, ListView):
    queryset = Ticket.objects.all().filter(status="Fait")
    template_name = "ticket/vues/fait.html"

class TicketEnCours(LoginRequiredMixin, ListView):
    queryset = Ticket.objects.all().filter(status="En cours")
    template_name = "ticket/vues/en_cours.html"
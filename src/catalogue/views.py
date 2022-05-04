from .models import *
from utilisateur.models import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView

def index(request):
	adresses = GeoRefPostalAddress.objects.all()
	context = {'adresses':adresses}
	return render(request, 'catalogue/accueil.html', context)

#########
# CUBIM #
#########
class CubimView(TemplateView):
	template_name = "catalogue/cubim/accueil.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class TfcView(TemplateView):
	template_name = "catalogue/cubim/projet1.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projet = kwgOrganization.objects.all().get(name="Académie des Beaux-Arts de la Ville de Tournai")
		context['projet'] = projet
		context['adresse'] = GeoRefPostalAddress.objects.all().get(of_organization=projet.identification)
		return context
########
# FASE #
########
class EtabListView(ListView):
	queryset = EtablissementEnseignement.objects.all().filter(roles=2)
	template_name = "catalogue/fase/etab_list.html"
	
class PoListView(ListView):
	queryset = EtablissementEnseignement.objects.all().filter(roles=1)
	template_name = "catalogue/fase/po_list.html"

class FaseListView(ListView):
	model = EtablissementEnseignement
	template_name = "catalogue/fase/fase_list.html"
	paginate_by = 10

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['total'] = EtablissementEnseignement.objects.all().count()
		context['total_po'] = kwgOrganization.objects.all().filter(roles=1).count()
		context['total_etab'] = kwgOrganization.objects.all().filter(roles=2).count()
		return context

class OrganizationListView(ListView):
	model = kwgOrganization
	template_name = "catalogue/crud/organization/organization_list.html"
	paginate_by = 10

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['total'] = kwgOrganization.objects.all().count()
		return context

class OrganizationDetailView(DetailView):
	model = kwgOrganization
	fields = '__all__'
	template_name = "catalogue/crud/organization/organization_details.html"

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['adresses'] = kwgPostalAddress.objects.all().filter(of_organization=self.object)
		context['relations'] = kwgOrganizationRelationship.objects.all().filter(relating_organization_id=self.object)
		context['depend_de'] = kwgOrganizationRelationship.objects.all().filter(related_organization=self.object)
		context['fase'] =  EtablissementEnseignement.objects.all().filter(kwgorganization_ptr_id=self.object)
		return context


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

def gestion(request):
	return render(request, "catalogue/gestion.html")

#########
# CUBIM #
#########
class VueUpdateLocalisation(UpdateView):
	model = GeoRefPostalAddress
	template_name = "catalogue/crud/localisation/localisation_ajout.html"
	fields = "__all__"
	success_url = reverse_lazy('catalogue:localisations-list')

class VueCreateLocalisation(CreateView):
	model = GeoRefPostalAddress
	template_name = "catalogue/crud/localisation/localisation_ajout.html"
	fields = "__all__"

class VueDetailLocalisation(DetailView):
	model = GeoRefPostalAddress
	template_name = "catalogue/crud/localisation/localisation_details.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['occupants'] = kwgPostalAddress.objects.all().filter(id=self.object.kwgpostaladdress_ptr_id)
		return context

class VueListLocalisation(ListView):
	model = GeoRefPostalAddress
	template_name = "catalogue/crud/localisation/localisation_list.html"

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
		context['adresses'] = ImplantationScolaire.objects.all().filter(georefpostaladdress_ptr_id__kwgpostaladdress_ptr_id__of_organization=projet.identification)
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
		adresses = kwgPostalAddress.objects.all().filter(of_organization=self.object)
		context['implantations'] = ImplantationScolaire.objects.all().filter(georefpostaladdress_ptr_id__kwgpostaladdress_ptr_id__of_organization=self.object)
		context['adresses'] = adresses
		context['relations'] = kwgOrganizationRelationship.objects.all().filter(relating_organization_id=self.object)
		context['depend_de'] = kwgOrganizationRelationship.objects.all().filter(related_organization=self.object)
		context['fase'] =  EtablissementEnseignement.objects.all().filter(kwgorganization_ptr_id=self.object)
		return context

class OrganizationUpdateView(UpdateView):
	model = kwgOrganization
	fields = '__all__'
	template_name = "catalogue/crud/organization/organization_ajout.html"
	success_url = "/catalogue/organisation/{identification}/"

class OrganizationCreateView(CreateView):
	model = kwgOrganization
	fields = '__all__'
	template_name = "catalogue/crud/organization/organization_ajout.html"
from .models import *
from utilisateur.models import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

def index(request):
	adresses = GeoRefPostalAddress.objects.all()
	context = {'adresses':adresses}
	return render(request, 'catalogue/accueil.html', context)

class EtabEnsListView(ListView):
	model = EtablissementEnseignement
	template_name = "catalogue/crud/organization/etabens_list.html"
	paginate_by = 10

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['total'] = EtablissementEnseignement.objects.all().count()
		context['total_po'] = kwgOrganization.objects.filter(roles=1).count()
		context['total_etab'] = kwgOrganization.objects.filter(roles=2).count()
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
		context['adresses'] = GeoRefPostalAddress.objects.all().filter(of_organization=self.object)
		context['relations'] = kwgOrganizationRelationship.objects.all().filter(relating_organization=self.object)
		context['depend_de'] = kwgOrganizationRelationship.objects.all().filter(related_organization=self.object)
		context['fase'] =  EtablissementEnseignement.objects.all().filter(kwgorganization_ptr_id=self.object)
		return context


from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from .models import *
 
def index(request):
	a_approuver = Document.objects.all().filter(validation="AA")
	approuve = Document.objects.all().filter(validation="A")
	approuve_commente = Document.objects.all().filter(validation="AC")
	non_approuve = Document.objects.all().filter(validation="NA")

	conception = Document.objects.all().filter(etat=0)
	partage = Document.objects.all().filter(etat=1)
	publication = Document.objects.all().filter(etat=2)
	archivage = Document.objects.all().filter(etat=3)
	context = {
		"a_approuver":a_approuver,
		"approuve":approuve,
		"approuve_commente":approuve_commente,
		"non_approuve":non_approuve,
		"conception":conception,
		"partage":partage,
		"publication":publication,
		"archivage":archivage
		}
	return render(request, 'rudi/accueil.html', context)

class ValidationAApprouver(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(validation="AA")
	template_name = "rudi/vues/validation/a_approuver.html"

class ValidationApprouve(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(validation="A")
	template_name = "rudi/vues/validation/approuve.html"

class ValidationApprouveEtCommente(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(validation="AC")
	template_name = "rudi/vues/validation/approuve_commente.html"

class ValidationNonApprouve(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(validation="NA")
	template_name = "rudi/vues/validation/non_approuve.html"

class VueConception(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(etat=0)
	template_name = "rudi/vues/statut/conception.html"

class VueArchivage(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(etat=3)
	template_name = "rudi/vues/statut/archivage.html"

class VuePartage(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(etat=1)
	template_name = "rudi/vues/statut/partage.html"

class VuePublication(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(etat=2)
	template_name = "rudi/vues/statut/publication.html"

class DocDetailView(LoginRequiredMixin, DetailView):
	model = Document
	template_name = "rudi/crud/doc_details.html"

class DocCreateView(LoginRequiredMixin, CreateView):
	model = Document
	template_name = "rudi/crud/doc_ajout.html"
	fields = "__all__"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#context['']
		return context

class DocListView(LoginRequiredMixin, ListView):
	model = Document
	template_name = "rudi/crud/docs_list.html"

class DocUpdateView(LoginRequiredMixin, UpdateView):
	model = Document 
	template_name = "rudi/crud/doc_ajout.html"
	fields = "__all__"

class DocDeleteView(LoginRequiredMixin, DeleteView):
	model = Document
	template_name = "objet_a_effacer.html"
	success_url = "/rudi/documents/"
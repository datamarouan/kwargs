from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from .models import *

def index(request):
	return render(request, 'drive/accueil.html')

class ValidationAApprouver(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(validation="AA")
	template_name = "drive/vues/validation/a_approuver.html"

class ValidationApprouve(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(validation="A")
	template_name = "drive/vues/validation/approuve.html"

class ValidationApprouveEtCommente(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(validation="AC")
	template_name = "drive/vues/validation/approuve_commente.html"

class ValidationNonApprouve(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(validation="NA")
	template_name = "drive/vues/validation/non_approuve.html"

class VueConception(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(etat=0)
	template_name = "drive/vues/statut/conception.html"

class VueArchivage(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(etat=3)
	template_name = "drive/vues/statut/archivage.html"

class VuePartage(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(etat=1)
	template_name = "drive/vues/statut/partage.html"

class VuePublication(ListView, LoginRequiredMixin):
	queryset = Document.objects.all().filter(etat=2)
	template_name = "drive/vues/statut/publication.html"

class DocDetailView(DetailView, LoginRequiredMixin):
	model = Document
	template_name = "drive/crud/doc_details.html"

class DocCreateView(CreateView, LoginRequiredMixin):
	model = Document
	template_name = "drive/crud/doc_ajout.html"
	fields = "__all__"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#context['']
		return context

class DocListView(ListView, LoginRequiredMixin):
	model = Document
	template_name = "drive/crud/docs_list.html"

class DocUpdateView(UpdateView, LoginRequiredMixin):
	model = Document 
	template_name = "drive/crud/doc_ajout.html"
	fields = "__all__"

class DocDeleteView(DeleteView, LoginRequiredMixin):
	model = Document
	template_name = "objet_a_effacer.html"
	success_url = "/drive/documents/"
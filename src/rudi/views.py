from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from .models import *
  
def index(request):
	recent_files = Document.objects.all().order_by('pk')[:5]
	pdf_file = Document.objects.all().filter(fichier__endswith=".pdf")
	rvt_file = Document.objects.all().filter(fichier__endswith=".rvt")
	ifc_file = Document.objects.all().filter(fichier__endswith=".ifc")
	jpy_file = Document.objects.all().filter(fichier__endswith=".ipynb")
	doc = Q(fichier__endswith=".doc")
	docx = Q(fichier__endswith=".docx")
	odt = Q(fichier__endswith=".odt")
	xls = Q(fichier__endswith=".xls")
	xlsx = Q(fichier__endswith=".xlsx")
	ods = Q(fichier__endswith=".ods")
	doc_file = Document.objects.all().filter(doc | docx | odt)
	xls_file = Document.objects.all().filter(xls | xlsx | ods)
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
		"archivage":archivage,
		"pdf_file":pdf_file,
		"rvt_file":rvt_file,
		"ifc_file":ifc_file,
		"jpy_file":jpy_file,
		"doc_file":doc_file,
		"xls_file":xls_file,
		"recent_files":recent_files
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
	template_name = "rudi/vues/conception.html"

class VueArchivage(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(etat=3)
	template_name = "rudi/vues/archivage.html"

class VuePartage(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(etat=1)
	template_name = "rudi/vues/partage.html"

class VuePublication(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(etat=2)
	template_name = "rudi/vues/publication.html"

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

class PDFListView(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(fichier__endswith=".pdf")
	template_name = "rudi/vues/pdf_files.html"

class RVTListView(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(fichier__endswith=".rvt")
	template_name = "rudi/vues/rvt_files.html"

class XLSListView(LoginRequiredMixin, ListView):
	xls = Q(fichier__endswith=".xls")
	xlsx = Q(fichier__endswith=".xlsx")
	ods = Q(fichier__endswith=".ods")
	queryset = Document.objects.all().filter(xls | xlsx | ods)
	template_name = "rudi/vues/xls_files.html"

class DOCListView(LoginRequiredMixin, ListView):
	doc = Q(fichier__endswith=".doc")
	docx = Q(fichier__endswith=".docx")
	odt = Q(fichier__endswith=".odt")
	queryset = Document.objects.all().filter(doc | docx | odt)
	template_name = "rudi/vues/doc_files.html"

class IFCListView(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(fichier__endswith=".ifc")
	template_name = "rudi/vues/ifc_files.html"

class JPYListView(LoginRequiredMixin, ListView):
	queryset = Document.objects.all().filter(fichier__endswith=".ipynb")
	template_name = "rudi/vues/ipynb_files.html"

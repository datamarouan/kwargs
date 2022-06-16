from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from .models import *
from projet.models import Projet, Tache
from .utils import totemisage
from django.conf import settings
from wsgiref.util import FileWrapper

import ifcopenshell as ifc
import ifcopenshell.util
import ifcopenshell.util.element
import os, magic

def file_path_mime(file_path):
    return magic.from_file(file_path, mime=True)

def livrables(request, pk):
	document = Document.objects.all().get(id=pk)
	fichier = document.fichier.path
	mime = file_path_mime(fichier)
	with open(fichier, 'rb') as f:
		#file_data = FileWrapper(f)
		response = HttpResponse(f, content_type=mime)
		response['Content-Disposition'] = 'attachment; filename='+document.get_doc_name()+document.get_doc_extension()
	return response		

def totemification(request, slug):
	if request.method == "GET":
		document = Document.objects.all().get(slug=slug)
		fichier = document.fichier
		file_ifc= totemisage(fichier.path)
		file_ifc.write("tempote.ifc")
		file_location = settings.BASE_DIR / "tempote.ifc"
		with open(file_location, "r") as f:
			file_data = f.read()
			response = HttpResponse(file_data, content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename='+document.get_doc_name()+'_TOTEMIZE.ifc'
		return response

class TotemCorrectionView(LoginRequiredMixin, DetailView):
	model = Document
	template_name = "rudi/vues/totem.html"

class IfcAnalyseView(LoginRequiredMixin, DetailView):
	model = Document 
	template_name = "rudi/vues/analyse_ifc.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ifc_file = ifc.open(self.object.fichier.path)
		owner = ifc_file.by_type("IfcOwnerHistory")[0][0][0][2]
		app = ifc_file.by_type("IfcOwnerHistory")[0][1][2]
		superficies = {}
		surfaces = []
		for local in ifc_file.by_type("IfcSpace"):
			props = ifcopenshell.util.element.get_psets(local)
			for pset in get_related_property_sets(local):
				for propriete in pset.HasProperties:
					if propriete.Name == "NetPlannedArea":
						valeur = propriete.NominalValue.wrappedValue
						superficies["code"] = local.Name
						superficies["nom"] = local[7]
						superficies["surface"] = valeur
						surfaces.append(superficies.copy())
		context['surfaces'] = surfaces
		context['owner'] = owner
		context['application'] = app
		return context
  
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

class DocAttacheCreateView(LoginRequiredMixin, CreateView):
	model = Document
	template_name = "rudi/crud/doc_ajout.html"
	fields = "__all__"

	def form_valid(self, form):
		response = super().form_valid(form)
		context = {'pk':self.kwargs['pk']}
		dok = form.instance
		projet = Projet.objects.all().get(id=self.kwargs['pk'])
		projet.docz.add(dok)
		return response

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		return context

class DocCreateView(LoginRequiredMixin, CreateView):
	model = Document
	template_name = "rudi/crud/doc_ajout.html"
	fields = "__all__"

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
	success_url = "/cde/documents/"

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

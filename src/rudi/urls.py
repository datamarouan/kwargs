from django.urls import path
from . import views
 
app_name = 'rudi'

urlpatterns = [
	path("documents/", views.DocListView.as_view(), name="docs-list"),
	path('', views.index, name='index'),
	path('document/ajout/', views.DocCreateView.as_view(), name="new-doc"),
	path('document/<int:pk>/download/', views.livrables, name="download_livrable"),
	path('projet/<int:pk>/ajout/document/', views.DocAttacheCreateView.as_view(), name="new-doc-to-project"),

	path("documents/pdf/", views.PDFListView.as_view(), name="pdf-list"),
	path("documents/ifc/", views.IFCListView.as_view(), name="ifc-list"),

	path("documents/doc/", views.DOCListView.as_view(), name="doc-list"),
	path("documents/rvt/", views.RVTListView.as_view(), name="rvt-list"),
	path("documents/ipynb/", views.JPYListView.as_view(), name="ipynb-list"),
	path("documents/xls/", views.XLSListView.as_view(), name="xls-list"),
	
	path("documents/conception/", views.VueConception.as_view(), name="conception-list"),
	path("documents/archivage/", views.VueArchivage.as_view(), name="archivage-list"),
	path("documents/partage/", views.VuePartage.as_view(), name="partage-list"),
	path("documents/publication/", views.VuePublication.as_view(), name="publication-list"),

	path("documents/a_approuver/", views.ValidationAApprouver.as_view(), name="a-approuver"),
	path("documents/approuve/", views.ValidationApprouve.as_view(), name="approuve"),
	path("documents/approuve_commente/", views.ValidationApprouveEtCommente.as_view(), name="approuve-commente"),
	path("documents/non_approuve/", views.ValidationNonApprouve.as_view(), name="non-approuve"),
	
	path("document/<str:slug>/", views.DocDetailView.as_view(), name="doc-details"),
	path("document/<str:slug>/edition/", views.DocUpdateView.as_view(), name="doc-modif"),
	path("document/<str:slug>/delete/", views.DocDeleteView.as_view(), name="doc-delete"),

	path("documents/<str:slug>/analyse/", views.IfcAnalyseView.as_view(), name="analyse_ifc"),
	path("document/<str:slug>/totem/", views.TotemCorrectionView.as_view(), name="correction_totem"),
	path('document/<str:slug>/totem/corrige', views.totemification, name="totem_correction"),
]

from django.urls import path
from . import views

app_name = 'drive'

urlpatterns = [
	path('', views.index, name='index'),
	path('document/ajout/', views.DocCreateView.as_view(), name="new-doc"),
	path("documents/", views.DocListView.as_view(), name="docs-list"),
	
	path("documents/conception/", views.VueConception.as_view(), name="conception-list"),
	path("documents/archivage/", views.VueArchivage.as_view(), name="archivage-list"),
	path("documents/partage/", views.VuePartage.as_view(), name="partage-list"),
	path("documents/publication/", views.VuePublication.as_view(), name="publication-list"),

	path("documents/a_approuver/", views.ValidationAApprouver.as_view(), name="a-approuver"),
	path("documents/approuve/", views.ValidationApprouve.as_view(), name="approuve"),
	path("documents/approuve_commente/", views.ValidationApprouveEtCommente.as_view(), name="approuve-commente"),
	path("documents/non_approuve/", views.ValidationNonApprouve.as_view(), name="non-approuve"),
	
	path("document/<str:pk>/", views.DocDetailView.as_view(), name="doc-details"),
	path("document/<str:pk>/edition/", views.DocUpdateView.as_view(), name="doc-modif"),
	path("document/<str:pk>/delete/", views.DocDeleteView.as_view(), name="doc-delete"),
]

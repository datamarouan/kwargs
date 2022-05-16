from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
	path('', views.index, name='index'),
	path('organisations/', views.OrganizationListView.as_view(), name="orga-list"),
	path("fase/", views.FaseListView.as_view(), name="fase-list"),
	path("cubim/", views.CubimView.as_view(), name="cubim"),
	path("cubim/tfc/", views.TfcView.as_view(), name="tfc"),
	path("organisation/<str:pk>/", views.OrganizationDetailView.as_view(), name="orga-details"),
	path("organisation/<str:pk>/edition/", views.OrganizationUpdateView.as_view(), name="orga-modif"),
	path("organisation/ajout/", views.OrganizationCreateView.as_view(), name="nouvel-orga"),
	path("localisation/<int:pk>/", views.VueDetailLocalisation.as_view(), name="localisation-details"),
	path("localisation/ajout/", views.VueCreateLocalisation.as_view(), name="localisation-ajout"),
	path("localisation/<int:pk>/edition/", views.VueUpdateLocalisation.as_view(), name="localisation-modif"),
	path('pouvoirs_organisateurs/', views.PoListView.as_view(), name='po-list'),
	path('etablissements_enseignement/', views.EtabListView.as_view(), name='etab-list'),
	path("localisations/", views.VueListLocalisation.as_view(), name="localisations-list"),
	path("gestion/", views.gestion, name="gestion-du-site")
]
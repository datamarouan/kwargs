from django.urls import path
from . import views

app_name = 'projet'

urlpatterns = [
	path('', views.index, name='index'),
	path('ajout/', views.ProjetCreateView.as_view(), name="new-projet"),
	path('<int:pk>/', views.ProjetDetailView.as_view(), name="projet-details"),
	path('<int:pk>/edition/', views.ProjetUpdateView.as_view(), name="projet-modif"),
	path("<int:pk>/deletion/", views.ProjetDeleteView.as_view(), name="projet-delete"),
	path('tache/ajout/', views.TacheCreateView.as_view(), name="new-tache"),
	path("tache/<int:pk>/", views.TacheDetailView.as_view(), name="tache-details"),
	path("tache/<int:pk>/edition/", views.TacheUpdateView.as_view(), name="tache-modif"),
	path("tache/<int:pk>/deletion/", views.TacheDeleteView.as_view(), name="tache-delete"),
]
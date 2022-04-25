from django.urls import path
from . import views

app_name = "glossaire"

urlpatterns = [
	path('', views.TermeListView.as_view(template_name = "glossaire/accueil.html"), name='index'),
    path('termes/', views.TermeListView.as_view(template_name = "glossaire/crud/terms_list.html"), name='terms-list'),
    path('terme/ajout/', views.TermeCreateView.as_view(), name="terme-ajout"),
    path('terme/<slug:slug>/', views.TermeDetailView.as_view(), name="terme-details"),
	path('terme/<slug:slug>/edition/', views.TermeUpdateView.as_view(), name="terme-modif"),
    path('terme/<slug:slug>/delete/', views.TermeDeleteView.as_view(), name="terme-delete"),
    path('source/ajout/', views.SourceCreateView.as_view(), name="source-ajout"),
]

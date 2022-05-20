from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
	path('', views.index, name='index'),
	path('tickets/', views.index, name='index'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name="ticket-details"),
    path('ticket/ajouter/', views.TicketCreateView.as_view(), name="new-ticket"),
    path('ticket/<int:pk>/edition/', views.TicketUpdateView.as_view(), name="ticket-modif"),
    path('ticket/<int:pk>/effacer/', views.TicketDeleteView.as_view(), name="ticket-delete"),
    path("tickets/a_faire/", views.TicketAFaire.as_view(), name="ticket-a-faire"),
    path("tickets/en_cours/", views.TicketEnCours.as_view(), name="ticket-en-cours"),
    path("tickets/fait/", views.TicketFait.as_view(), name="ticket-fait"),
]

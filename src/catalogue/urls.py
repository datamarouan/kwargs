from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
	path('', views.index, name='index'),
	path('organisations/', views.OrganizationListView.as_view(), name="orga-list"),
	path("fase/", views.FaseListView.as_view(), name="fase-list"),
	path("organisation/<str:pk>/", views.OrganizationDetailView.as_view(), name="orga-details"),
	path('pouvoirs_organisateurs/', views.PoListView.as_view(), name='po-list'),
	path('fase/<str:pk>/', views.FaseDetailView.as_view(), name='fase-details')
]
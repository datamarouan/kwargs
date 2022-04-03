from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
	path('', views.index, name='index'),
	path('organisations/', views.OrganizationListView.as_view(), name="orga-list"),
	path("organisations/<str:pk>/", views.OrganizationDetailView.as_view(), name="orga-details")
]
from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    path('', views.index, name='accueil'),
    path('contact/', views.contact, name='contact'),
]

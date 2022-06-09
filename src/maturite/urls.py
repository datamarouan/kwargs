from django.urls import path
from . import views

app_name = 'maturite'

urlpatterns = [
	path('', views.index, name='index'),
]
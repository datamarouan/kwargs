from django.contrib import admin
from projet.models import Projet, Tache

admin.site.register([Projet, Tache])

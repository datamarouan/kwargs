from django.contrib import admin
from utilisateur.models import kwgPerson, kwgActorRole

admin.site.register([kwgPerson, kwgActorRole])

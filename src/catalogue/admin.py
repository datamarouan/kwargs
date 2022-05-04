from django.contrib import admin
from .models import *

admin.site.register([
	kwgOrganization, 
	kwgPostalAddress,
	kwgTelecomAddress,
	kwgPersonAndOrganization,
	kwgOrganizationRelationship,
	kwgApplication,
	kwgOwnerHistory,
	EtablissementEnseignement,
	GeoRefPostalAddress,
	ImplantationScolaire
	])

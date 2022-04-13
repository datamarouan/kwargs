import uuid
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utilisateur.models import *

#####################
# I. RESOURCE LAYER #
#####################
######################
# I.1. ActorResource #
######################
class kwgAddress(models.Model):

	class kwgAddressTypeEnum(models.TextChoices):
		"""IfcAddressTypeEnum"""
		OFFICE = "O", _("Bureau")
		SITE = "S", _("Site")
		HOME = "H", _("Domicile")
		DISTRIBUTIONPOINT = "D", _("Point de distribution postal")
		USERDEFINED = "UD", ("Défini par l'utilisateur")

	purpose = models.CharField(
		max_length=2,
		choices=kwgAddressTypeEnum.choices,
		help_text="Identifies the logical location of the address")
	description = models.TextField(blank=True, null=True)
	user_defined_purpose = models.CharField(max_length=255, blank=True, null=True)
	of_person = models.ManyToManyField('utilisateur.kwgPerson', blank=True)
	of_organization = models.ManyToManyField('kwgOrganization', blank=True)

	class Meta:
		abstract=True

	def clean(self):
		if self.role=="UD" and not self.user_defined_purpose:
			raise ValidationError("	Either attribute value Purpose is not given, or when attribute Purpose has enumeration value USERDEFINED then attribute UserDefinedPurpose shall also have a value.")

class kwgPostalAddress(kwgAddress):
	"""This entity represents an address for delivery of paper based mail and other postal deliveries"""
	internal_location = models.CharField(max_length=255, blank=True, null=True,
		help_text="An organization defined address for internal mail delivery")
	addresses_lines = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adresse")
	postal_box = models.CharField(max_length=255, blank=True, null=True, verbose_name="Boîte postale")
	town = models.CharField(max_length=255, blank=True, null=True, verbose_name="Localité")
	region = models.CharField(max_length=255, blank=True, null=True)
	postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Code postal")
	country = models.CharField(max_length=255, blank=True, null=True, default="Belgique", verbose_name="Pays")

	def clean(self):
		"""Requires that at least one attribute of internal location, 
		address lines, town, region or country is asserted. It is not acceptable
		 to have a postal address without at least one of these values."""
		if not (self.internal_location 
			or self.addresses_lines 
			or self.postal_box 
			or self.town 
			or self.region
			or self.postal_code
			or self.country):
			raise ValidationError("It is not acceptable to have a postal address without at least one of these values.")

	class Meta:
		ordering = ('postal_code','addresses_lines')
		verbose_name = "Adresse Postale"
		verbose_name_plural = "Adresses postales"

	def __str__(self):
		return self.addresses_lines+" - "+str(self.postal_code)+" "+self.town

class GeoRefPostalAddress(kwgPostalAddress):
	# Coordonnées WSG84
	latitude = models.FloatField(editable=False, default=0)
	longitude = models.FloatField(editable=False, default=0)

	def latitude_longitude(self):
		"""Définition des latitude et longitude de l'Adresse."""
		geoloc = Here(apikey=env('HERE_APIKEY'))
		try:
			loc = geoloc.geocode(self.addresses_lines+', '+self.town).raw['Location']['NavigationPosition'][0]
			return (loc['Latitude'], loc['Longitude'])
		except:
			return (0,0)

	def save(self, *args,**kwargs):
		self.latitude, self.longitude = self.latitude_longitude()
		return super().save(*args,**kwargs)

	class Meta:
		verbose_name = "Adresse postale géoréférencée"
		verbose_name_plural = "Adresses postales géoréférencées"

class kwgTelecomAddress(kwgAddress):
	"""This entity represents an address to which telephone, electronic 
	mail and other forms of telecommunications should be addressed."""
	telephone_numbers = models.CharField(max_length=255, blank=True, null=True)
	mobile_numbers = models.CharField(max_length=255, blank=True, null=True)
	# PagerNumber
	electronic_mail_addresses = models.EmailField(blank=True, null=True)
	www_home_page_url = models.URLField(blank=True, null=True)
	# MessagingIDs

	def clean(self):
		if not (self.telephone_numbers 
			or self.mobile_numbers 
			or self.electronic_mail_addresses 
			or self.www_home_page_url):
			raise ValidationError("It is not acceptable to have a telecommunications address without at least one of these values.")

	def __str__(self):
		if self.telephone_numbers:
			return self.telephone_numbers
		elif self.mobile_numbers:
			return self.mobile_numbers
		elif self.electronic_mail_addresses:
			return self.electronic_mail_addresses
		else:
			return selfwww_home_page_url


	class Meta:
		verbose_name = "Adresse Telecom"
		verbose_name_plural = "Adresses Telecom"

class kwgOrganization(models.Model):
	'''A named and structured grouping with a corporate identity.
	The relationships between IfcOrganization's, like between department within a company, 
	can be expressed using the objectified relationship IfcOrganizationRelationship.
	Entity adapted from organization defined in ISO 10303-41. '''
	identification = models.CharField(max_length=36,primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	roles=models.ManyToManyField('utilisateur.kwgActorRole')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("catalogue:orga-details", args=[self.identification])

	class Meta:
		ordering = ('name',)
		verbose_name = "Organisation"
		verbose_name_plural = "Organisations"

class EtablissementEnseignement(kwgOrganization):
	"""Fichier signalétique des établissements d'enseignement 
	de la Fédération Wallonie-Bruxelles (FASE)"""
	fase=models.CharField(max_length=6, blank=True, null=True)
	bce = models.CharField(max_length=15,blank=True, null=True)
	reseau = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		verbose_name = "Etablissement d'enseignement"
		verbose_name_plural = "Etablissements d'enseignement"

class kwgPersonAndOrganization(models.Model):
	"""This entity represents a person acting on behalf of an organization.
	Entity adapted from person_and_organization defined in ISO 10303-41."""
	the_person = models.ForeignKey(kwgPerson, on_delete=models.CASCADE, related_name="engaged_in")
	the_organization = models.ManyToManyField(kwgOrganization, related_name="engages")
	roles=models.ManyToManyField('utilisateur.kwgActorRole')

	class Meta:
		verbose_name = "Personne agissant au nom d'une Organisation"
		verbose_name_plural = "Personnes agissant au nom d'une Organisation"

	def __str__(self):
		return self.the_person.family_name+", "+self.the_person.given_name+" agissant au nom de "+", ".join(self.the_organization.all().values_list('name', flat=True))
##################################
# I.2. ExternalReferenceResource #
##################################
class kwgResourceLevelRelationship(models.Model):
	"""IfcResourceLevelRelationship is an abstract base entity for relationships between resource-level entities."""
	name = models.CharField(max_length=255, blank=True, null=True, help_text="A name used to identify or qualify the relationship.")
	description = models.TextField(blank=True)

	class Meta:
		abstract = True

class kwgOrganizationRelationship(kwgResourceLevelRelationship):
	relating_organization = models.ForeignKey(kwgOrganization, on_delete=models.CASCADE, related_name="relates")
	related_organization = models.ManyToManyField(kwgOrganization, related_name="is_related_by")

	class Meta:
		verbose_name = "Relation entre organisations"
		verbose_name_plural = "Relations entre organisations"

	def __str__(self):
		return self.relating_organization.name+" >> "+self.name+" >> "+" - ".join(self.related_organization.all().values_list('name', flat=True))
		# return "Relations entre "+self.relating_organization.name+" et "+", ".join(self.related_organization.all().values_list('name', flat=True))
########################
# I.3. UtilityResource #
########################
class kwgApplication(models.Model):
	"""IfcApplication holds the information about an IFC compliant application developed by 
	an application developer. The IfcApplication utilizes a short identifying name as provided 
	by the application developer."""
	application_developper = models.ForeignKey(kwgOrganization, on_delete=models.DO_NOTHING)
	version = models.CharField(max_length=12)
	application_full_name = models.CharField(max_length=124)
	application_identifier = models.CharField(max_length=124, unique=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=["application_full_name","version"], name="unique_application")]
		verbose_name = "Application"

class kwgOwnerHistory(models.Model):
	"""IfcOwnerHistory defines all history and identification related information. 
	In order to provide fast access it is directly attached to all independent objects, 
	relationships and properties. IfcOwnerHistory is used to identify the creating and owning 
	application and user for the associated object, as well as capture the last modifying 
	application and user."""
	class kwgStateEnum(models.IntegerChoices):
		"""Enumeration that defines the current access state of the object."""
		READWRITE = 1 # Object is in a Read-Write state. It may be modified by an application.
		READONLY = 2 # Object is in a Read-Only state. It may be viewed but not modified by an application.
		LOCKED = 3 # Object is in a Locked state. It may not be accessed by an application.
		READWRITELOCKED = 4 # Object is in a Read-Write-Locked state. It may not be accessed by an application.
		READONLYLOCKED = 5	# Object is in a Read-Only-Locked state. It may not be accessed by an application.
	class kwgChangeActionEnum(models.IntegerChoices):
		"""IfcChangeActionEnum identifies the type of change that might have 
		occurred to the object during the last session (for example, added, 
		modified, deleted)."""
		NOCHANGE = 1 # Object has not been modified.
		MODIFIED = 2 # A modification to the object has been made by the user 
		# and application defined by the LastModifyingUser and 
		# LastModifyingApplication respectively.
		ADDED = 3 # The object has been created by the user and application 
		# defined by the OwningUser and OwningApplication respectively.
		DELETED = 4 # The object has been deleted by the user and application 
		# defined by the LastModifyingUser and LastModifyingApplication respectively.
		NOTDEFINED = 5 # The change action is not known or has not been defined.
	owning_user = models.ForeignKey(kwgPersonAndOrganization, on_delete=models.CASCADE, related_name="user_owning")
	owning_application = models.ForeignKey(kwgApplication, on_delete=models.CASCADE, related_name="app_owning")
	state = models.IntegerField(choices=kwgStateEnum.choices, default=1)
	change_action = models.IntegerField(choices=kwgChangeActionEnum.choices, default=5)
	last_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
	last_modifying_user = models.ForeignKey(kwgPersonAndOrganization, on_delete=models.CASCADE, related_name="user_modifer")
	last_modifying_application = models.ForeignKey(kwgApplication, on_delete=models.CASCADE, related_name="app_modifer")
	creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	class Meta:
		verbose_name = "Historique Utilisateur"
		verbose_name_plural = "Historiques Utilisateur"
##################
# II. CORE LAYER #
##################


#####################
# III. SHARED LAYER #
#####################
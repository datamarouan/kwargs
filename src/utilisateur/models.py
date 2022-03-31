from django.contrib.auth.models import User
from PIL import Image
import uuid
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class kwgActorRole(models.Model):
	"""This entity indicates a role which is performed by an actor, either a person, 
	an organization or a person related to an organization.
	Entity adapted from organization_role and person_role defined in ISO 10303-41."""
	class kwgRoleEnum(models.TextChoices):
		"""IfcRoleEnum"""
		SUPPLIER = "SU", _("Fournisseur")
		MANUFACTURER = "MA", _("Fabricant")
		CONTRACTOR = "CO", _("Prestataire")
		SUBCONTRACTOR = "SB", _("Sous traitant")
		ARCHITECT = "AR", _("Architecte")
		STRUCTURALENGINEER = "SE", _("Ingénieur Structure/Stabilité")
		COSTENGINEER = "CE", _("Ingénieur Coûts")
		CLIENT = "CL", _("Client")
		BUILDINGOWNER = "BP", _("Propriétaire du bâtiment")
		BUILDINGOPERATOR = "BO", _("Opérateur du bâtiment")
		MECHANICALENGINEER = "ME", _("Ingénieur mécanique")
		ELECTRICALENGINEER = "EE", _("Ingénieur électricité")
		PROJECTMANAGER ="PM", _("Chef de projet")
		FACILITIESMANAGER = "FM", _("Facility Manager")
		CIVILENGINEER = "CI", _("Ingénieur civil")
		COMMISSIONINGENGINEER = "CN", _("Ingénieur mise en service")
		ENGINEER = "IR", _("Ingénieur")
		OWNER = "PR", _("Propriétaire")
		CONSULTANT = "CS", _("Consultant")
		CONSTRUCTIONMANAGER = "CP", _("Directeur des travaux")
		FIELDCONSTRUCTIONMANAGER = "CC", _("Chef de chantier")
		RESELLER = "RV", _("Revendeur")
		USERDEFINED = "UD", _("Défini par l'utilisateur")

	role = models.CharField(
		max_length=2, 
		choices=kwgRoleEnum.choices, 
		help_text="The name of the role played by an actor")
	user_defined_role = models.CharField(
		max_length=255,
		blank=True,
		help_text="Allows for specification of user defined roles beyond the enumeration values provided by Role attribute of type IfcRoleEnum")
	description = models.TextField(
		blank=True,
		help_text="A textual description rzelating the nature of the role played by an actor")

	def __str__(self):
		if self.role == "UD":
			return self.user_defined_role
		else:
			return self.get_role_display()

	# Remarque : CheckConstraints n'est pas pris en charge par MySql
	def clean(self):
		if self.role=="UD" and not self.user_defined_role:
			raise ValidationError("If the attribute Role has the enumeration value USERDEFINED then a value for the attribute UserDefinedRole shall be asserted.")

	class Meta:
		verbose_name = "Rôle d'acteur"
		verbose_name_plural = "Rôles d'acteur"

class kwgPerson(models.Model):
	"""This entity represents an individual human being.
	Entity adapted from person defined in ISO 10303-41"""
	identification = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personne")
	middle_name = models.CharField(max_length=255, blank=True, null=True, 
		help_text="Additional names given to a person that enable their identification apart from others who may have the same or similar family and given names",
		verbose_name="Autre(s) prénom(s)")
	prefix_titles=models.CharField(max_length=5, blank=True, null=True,
		help_text="The word, or group of words, which specify the person's social and/or professional standing and appear before his/her names")
	suffix_titles=models.CharField(max_length=5, blank=True, null=True,
		help_text="The word, or group of words, which specify the person's social and/or professional standing and appear before his/her names")
	roles=models.ManyToManyField('kwgActorRole')
	image = models.ImageField(default='default.jpg', upload_to='avatars/')

	
	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (150, 150)
			img.thumbnail(output_size)
			img.save(self.image.path)
	
	class Meta:
		#ordering = ('user.last_name',)
		verbose_name = "Personne"

	def __str__(self):
		if self.user.last_name and  self.user.first_name:
			return self.user.last_name+", "+self.user.first_name
		else:
			return self.user.username

	def clean(self):
		if not self.user.last_name and not self.user.first_name:
			raise ValidationError("Requires that the family name or/and the given name is provided as minimum information.")

		if (self.middle_name and not self.user.last_name) or (self.middle_name and not self.user.first_name):
			raise ValidationError("If middle names are provided, the family name or/ and the given name shall be provided too.")

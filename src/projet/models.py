from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from catalogue.models import GeoRefPostalAddress, kwgOrganization
from rudi.models import Document
from django.urls import reverse
from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords

STATUS = (
	(1, 'Stuck'),
	(2, 'Working'),
	(3, 'Done'),
)
DELAI = (
	(1, 'On Due'),
	(2, 'Overdue'),
	(3, 'Done'),
)
class Projet(models.Model):
	nom = models.CharField(max_length=124)
	description = models.TextField()
	assigne = models.ManyToManyField('auth.User', related_name="equipe")
	status = models.IntegerField(default=1, choices=STATUS)
	date_butoir = models.DateField()
	completude = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	localisation = models.ManyToManyField(GeoRefPostalAddress, related_name="endroits")
	docz = models.ManyToManyField(Document, related_name="documentation")
	client = models.ManyToManyField(kwgOrganization, related_name="client")
	tags = TaggableManager(verbose_name="Mots-clés", blank=True,
	help_text="Une liste de mots-clés séparés par une virgule, en minuscule")
	history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))

	def __str__(self):
		return self.nom

	def get_absolute_url(self):
		return reverse("projet:projet-details", args=[self.pk]) 

class Tache(models.Model):
	projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="tasks")
	assigne = models.ManyToManyField('auth.User')
	nom = models.CharField(max_length=80)
	status = models.IntegerField(default=1, choices=STATUS)
	date_butoir = models.DateField(null=True, blank=True)
	delai = models.IntegerField(default=1, choices=DELAI)
	docz = models.ManyToManyField(Document, related_name="documents_lies")
	tags = TaggableManager(verbose_name="Mots-clés", blank=True,
	help_text="Une liste de mots-clés séparés par une virgule, en minuscule")

	class Meta:
		ordering = ['projet', 'nom']

	def __str__(self):
		return self.nom

	def get_absolute_url(self):
		return reverse("projet:tache-details", args=[self.pk]) 
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from catalogue.models import GeoRefPostalAddress
from django.urls import reverse

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
	assigne = models.ManyToManyField('auth.User')
	status = models.IntegerField(default=1, choices=STATUS)
	date_butoir = models.DateField()
	completude = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	localisation = models.ManyToManyField(GeoRefPostalAddress)

	def __str__(self):
		return self.nom

	def get_absolute_url(self):
		return reverse("projet:projet-details", args=[self.pk]) 

class Tache(models.Model):
	projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="tasks")
	assigne = models.ManyToManyField('auth.User')
	nom = models.CharField(max_length=80)
	status = models.IntegerField(default=1, choices=STATUS)
	delai = models.IntegerField(default=1, choices=DELAI)

	class Meta:
		ordering = ['projet', 'nom']

	def __str__(self):
		return self.nom
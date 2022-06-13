from django.db import models
import os, uuid
from .utils import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from crum import get_current_user
from simple_history.models import HistoricalRecords

def get_doc_filename(instance, filename):
	base_name = os.path.basename(filename)
	name, ext = os.path.splitext(base_name)
	extension = ext.split('.')[1]
	if extension in ['jpg','jpeg','png','svg','tiff','gif','psd','eps','ai','bmp']:
		dossier = 'images'
	elif extension == 'dwg':
		dossier = 'plan_autocad'
	else:
		dossier = extension
	return "rudi/"+str(instance.get_etat_display().lower())+"/"+dossier+'/'+filename


class Document(models.Model):
	identification = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
	fichier = models.FileField(upload_to=get_doc_filename, max_length=255, verbose_name="Document")
	nom = models.CharField(max_length=125, help_text="Un nom courant du fichier", blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	class EtatTypeEnum(models.IntegerChoices):
		CONCEPTION = 0
		PARTAGE = 1
		PUBLICATION = 2
		ARCHIVAGE = 3
	etat = models.IntegerField(choices=EtatTypeEnum.choices, default=EtatTypeEnum.CONCEPTION)
	class ValidationTypeEnum(models.TextChoices):
		a_approuver = "AA", "A approuver" # le contenu de l’information n’a pas encore abordé le processus de validation
		approuve = "A", "Approuvé" # Le contenu de l’information a subi le processus de validation avec un résultat positif
		approuve_et_commente = "AC", "Approuvé et Commenté" # Bien que le processus de validation a été adopté avec succès, des insuffisances ont été constatées nécessitant des interventions obligatoires pour que l’utilisation soit réalisable aux fins prévues
		non_approuve = "NA", "Non Approuvé"
	validation = models.CharField(max_length=2, 
		choices=ValidationTypeEnum.choices, 
		default=ValidationTypeEnum.a_approuver) # Le processus de validation n’a pas abouti et exige une nouvelle élaboration du contenu de l’information.
	history = HistoricalRecords(
		history_change_reason_field=models.TextField(null=True)
		)

	def __str__(self):
		if self.nom:
			return self.nom
		else:
			return str(self.fichier).split("/")[-1]

	def get_doc_extension(self):
		base_name = os.path.basename(self.fichier.name)
		name, ext = os.path.splitext(base_name)
		return ext

	def get_doc_name(self):
		base_name = os.path.basename(self.fichier.name)
		name, ext = os.path.splitext(base_name)
		return name

	def get_absolute_url(self):
		return reverse("rudi:doc-details", args=[self.identification])



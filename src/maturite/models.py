from django.db import models


class Choix(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Choix"


class Question(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.CharField(max_length=65, choices=[("G","Générale"),
        ("S","Software"),
        ("HW","Hardware"),
        ("HU","Human"),
        ("O","Organisationnel"),
        ("DM","Data Management")], default="G")
    critere = models.CharField(max_length=125,default="")
    choix = models.ManyToManyField(Choix, related_name='questions_liees', blank=True)

    def __str__(self):
        return self.nom

class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name="reponses", null=True, blank=True)
    choix = models.ForeignKey(Choix, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.question.nom} - {self.choix.nom}"
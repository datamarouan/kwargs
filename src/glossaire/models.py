from django.db import models
from crum import get_current_user
from django.urls import reverse
from django.shortcuts import render
from django.utils.text import slugify
from tinymce.models import HTMLField
from taggit.managers import TaggableManager

class Cachet(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, editable=False,
    on_delete=models.SET_NULL, default=None, related_name='%(app_label)s_%(class)s_created')
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey('auth.User', blank=True, null=True, editable=False,
    on_delete=models.CASCADE, default=None, related_name='%(app_label)s_%(class)s_modified')

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        return super(Cachet, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Terme(Cachet):
    mot = models.CharField(max_length=150, verbose_name="Terme")
    desc = HTMLField(verbose_name="Définition(s)")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    tags = TaggableManager(verbose_name="Mots-clés", blank=True, help_text="Une liste de mots-clés séparés par une virgule, en minuscule")
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.mot

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self)
        return super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('glossaire:terme-details', args=[self.slug])

    class Meta:
        ordering = ('mot',)

class Source(Cachet):
    label = models.CharField(max_length=100)
    lien = models.URLField(max_length=255)
    terme = models.ManyToManyField('Terme', related_name="references")

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('label',)

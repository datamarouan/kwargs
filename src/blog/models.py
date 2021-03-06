from django.db import models
from crum import get_current_user
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils.text import slugify
from taggit.managers import TaggableManager
from PIL import Image


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

class Article(Cachet):
	titre = models.CharField(max_length=255, unique=True)
	intro = models.TextField(default="")
	contenu = HTMLField()
	slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)
	published = models.BooleanField(default=False, verbose_name="Publication immédiate ?")
	tags = TaggableManager(verbose_name="Mots-clés", blank=True,
	help_text="Une liste de mots-clés séparés par une virgule, en minuscule")
	image = models.ImageField(default='blog/default.jpg', upload_to='blog/')

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.titre

	def save(self,*args,**kwargs):

		self.slug = slugify(self.titre)
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 600:
			output_size = (200, 400)
			img.thumbnail(output_size)
			img.save(self.image.path)

	def get_absolute_url(self):
		return reverse('blog:article-details', args=[self.slug])

from django.db import models
from django.urls import reverse
from crum import get_current_user

class Ticket(models.Model):
	titre = models.CharField(max_length=100)
	assigne_a = models.ForeignKey('auth.User', null=True, blank = True, 
		on_delete=models.CASCADE, verbose_name="Assigné à", related_name='%(app_label)s_%(class)s_assigne')
	class TicketStatus(models.TextChoices):
		TO_DO = 'A faire'
		IN_PROGRESS = 'En cours'
		DONE = 'Fait'
	status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.TO_DO)
	description = models.TextField()
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	created_by = models.ForeignKey('auth.User', blank=True, null=True, editable=False,
	on_delete=models.SET_NULL, default=None, related_name='%(app_label)s_%(class)s_created')
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	modified_by = models.ForeignKey('auth.User', blank=True, null=True, editable=False,
	on_delete=models.CASCADE, default=None, related_name='%(app_label)s_%(class)s_modified')

	def __str__(self):
		return self.titre

	def get_absolute_url(self):
		return reverse("ticket:ticket-details", args=[self.pk])

	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and not user.pk:
			user = None
		if not self.pk:
			self.created_by = user
		self.modified_by = user
		return super(Ticket, self).save(*args, **kwargs)
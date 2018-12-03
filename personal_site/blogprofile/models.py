from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class ActiveUserManager(models.Manager):
	"""Query Profile of active user."""

	def get_queryset(self):
		"""Return query set of profiles for active users."""
		query = super(ActiveUserManager, self).get_queryset()
		return query.filter(user__is_active__exact=True)


class BlogProfile(models.Model):
	user = models.OneToOneField(
		User,
		related_name="profile",
		on_delete=models.CASCADE
	)
	address = models.CharField(max_length=255, blank=True, null=True)
	bio = models.TextField(default="")
	phone_number = models.CharField(max_length=12, blank=True, null=True)
	blog_id = models.UUIDField(default=uuid.uuid4, editable=False)
	active = ActiveUserManager()
	objects = models.Manager()

	def __str__(self):
		return """Username: {Username}
				  Address: {Address}
				  About Me: {AboutMe}
				  Phone: {Phone}""".format(
			Username=self.user.username,
			Address=self.address,
			AboutMe=self.bio,
			Phone=self.phone_number)

	@property
	def is_active(self):
		return self.user.is_active


@receiver(post_save, sender=User)
def make_user_profile(sender, instance, **kwargs):
	"""Instantiate a BlogProfile, connect to a new User instance, save that profile."""

	if kwargs["created"]:
		new_profile = BlogProfile(user=instance)
		new_profile.save()
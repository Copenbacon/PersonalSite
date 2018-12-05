"""Basic Blog Models. Entries and Albums."""
from django.db import models
from django.contrib.auth.models import User
from blogprofile.models import BlogProfile

PUBLISHED = [
    ('private', 'Private'),
    ('shared', 'Shared'),
    ('public', 'Public')
]

CATEGORY = [
	('fitness', 'Fitness'),
	('recipes', 'Recipes'),
	('maintenance', 'Maintenance')
]

class Entry(models.Model):
	"""Basic Blog Entry."""

	title = models.CharField(max_length=128)
	text = models.TextField(blank=True)
	created_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	description = models.CharField(max_length=255)
	date_uploaded = models.DateField(auto_now_add=True)
	date_modified = models.DateField(auto_now=True)
	date_published = models.DateTimeField(
		blank=True,
		null=True
    )
	published = models.CharField(
		max_length=15,
		choices=PUBLISHED,
		default='private'
    )
	category = models.CharField(
		max_length=15,
		choices=CATEGORY,
		default='fitness'
    )
	image_file = models.ImageField(upload_to='images')

	def __str__(self):
		"""Return title as string."""
		return self.title


class Album(models.Model):
	"""The Album class."""

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	date_uploaded = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	date_published = models.DateTimeField(
		blank=True,
		null=True)
	published = models.CharField(
		max_length=15,
		choices=PUBLISHED,
		default='private'
	)
	owner = models.ForeignKey(BlogProfile, related_name='albums',
		blank=True,
		null=True,
		on_delete=models.CASCADE)
	entries = models.ManyToManyField(
		"Entry",
		related_name="albums_of_entries",
		symmetrical=False)
	cover_image = models.ImageField(upload_to='images/cover_photos')

	def __str__(self):
		"""Return title as string."""
		return self.title

"""Test the Entry and Entry Album Models."""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Entry, Album
import factory

class UserFactory(factory.django.DjangoModelFactory):
	"""Create a bunch of fake users."""
	class Meta:
		model = User
		username = factory.Sequence(lambda n: "Blog User {}".format(n))
		email = factory.LazyAttribute(
		lambda x: "{}@datsite.com".format(x.username.replace(" ", ""))
    )

class EntryFactory(factory.django.DjangoModelFactory):
	"""Create a bunch of fake entries."""
	class Meta:
		model = Entry
		title = factory.Sequence(lambda n: "Entry {}".format(n))
		image_file = SimpleUploadedFile(name='image_1.jpg', content=open('imagersite/static/images/image_1.jpg', 'rb').read(), content_type='image/jpeg')


class AlbumFactory(factory.django.DjangoModelFactory):
	"""Create a bunch of fake Albums"""
	class Meta:
		model = Album
		title = factory.Sequence(lambda n: "Album {}".format(n))
		cover_image = SimpleUploadedFile(name='image_1.jpg', content=open('imagersite/static/images/image_1.jpg', 'rb').read(), content_type='image/jpeg')
		description = "Some Album"

class EntryTestCase(TestCase):
	"""Entry Test Class."""

	def setUp(self):
		"""User, entries, and album setup for tests."""
		self.users = [UserFactory.create() for i in range(10)]
		self.entry = [EntryFactory.create() for i in range(10)]
		self.album = [AlbumFactory.create() for i in range(10)]

	def test_entry_title(self):
		"""Test that entry has a title."""
		self.assertTrue("Entry" in Entry.objects.first().title)
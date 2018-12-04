"""Test the Entry and Entry Album Models."""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse_lazy
from blog.models import Entry, Album
from blogprofile.models import BlogProfile
import factory


class UserFactory(factory.django.DjangoModelFactory):
	"""Create a bunch of fake users."""

	class Meta:
		model = User
	username = factory.Sequence(lambda n: "Blog User {}".format(n))
	email = factory.LazyAttribute(lambda x: "{}@datsite.com".format(x.username.replace(" ", ""))
	)


class EntryFactory(factory.django.DjangoModelFactory):
	"""Create a bunch of fake entries."""

	class Meta:
		model = Entry
	title = factory.Sequence(lambda n: "Entry {}".format(n))
	image_file = SimpleUploadedFile(name='image_1.jpg', content=open('static/images/image_1.jpg', 'rb').read(), content_type='image/jpeg')


class AlbumFactory(factory.django.DjangoModelFactory):
	"""Create a bunch of fake Albums."""

	class Meta:
		model = Album
	title = factory.Sequence(lambda n: "Album {}".format(n))
	cover_image = SimpleUploadedFile(name='image_1.jpg', content=open('static/images/image_1.jpg', 'rb').read(), content_type='image/jpeg')
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

	def test_entry_has_description(self):
		"""Test that the Entry description field can be assigned."""
		entry = Entry.objects.first()
		entry.description = "This is a good entry."
		entry.save()
		self.assertTrue(Entry.objects.first().description == "This is a good entry.")

	def test_entry_has_published(self):
		"""Test the entry published field."""
		entry = Entry.objects.first()
		entry.published = 'public'
		entry.save()
		self.assertTrue(Entry.objects.first().published == "public")

	def test_entry_has_no_author(self):
		"""Test the entry instantiates with no author."""
		entry = Entry.objects.first()
		entry.save()
		self.assertFalse(entry.author)

	def test_entry_has_author(self):
		"""Test the entry can be assigned an author."""
		entry = Entry.objects.first()
		user1 = User.objects.first()
		entry.author = user1
		entry.save()
		self.assertTrue(entry.author)

	def test_author_has_entry(self):
		"""Test the entry published field."""
		entry1 = Entry.objects.first()
		user1 = User.objects.first()
		entry1.author = user1
		entry1.save()
		self.assertTrue(user1.profile == entry1.author.profile)
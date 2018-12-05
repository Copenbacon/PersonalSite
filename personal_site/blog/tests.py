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

	def test_album_exists(self):
		"""Album should exist."""
		album1 = Album.objects.first()
		self.assertTrue("Some Album" in album1.description)

	def test_album_has_cover_image(self):
		"""Album should have cover image."""
		album1 = Album.objects.first()
		self.assertTrue(album1.cover_image)

	def test_album_has_entry(self):
		"""Album should have an entry after adding one."""
		album1 = Album.objects.first()
		entry1 = Entry.objects.first()
		album1.entries.add(entry1)
		entry1.save()
		self.assertTrue(album1.entries.count() == 1)

	def test_album_has_no_owner_at_instantiation(self):
		"""Album should have no owner when started."""
		album1 = Album.objects.first()
		album1.entries.add(Entry.objects.first())
		self.assertFalse(album1.owner)

	def test_album_can_store_an_owner(self):
		"""Album should be assigned an owner."""
		album1 = Album.objects.first()
		entry1 = Entry.objects.first()
		album1.entries.add(entry1)
		user1 = User.objects.first()
		entry1.author = user1
		entry1.save()
		album1.owner = user1.profile
		self.assertTrue(album1.owner)

	def test_album_owner_is_blogprofile(self):
		"""Album should be assigned an owner."""
		album1 = Album.objects.first()
		entry1 = Entry.objects.first()
		album1.entries.add(entry1)
		user1 = User.objects.first()
		entry1.author = user1
		entry1.save()
		album1.owner = user1.profile
		self.assertTrue(album1.owner == entry1.author.profile)
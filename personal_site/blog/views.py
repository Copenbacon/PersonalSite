"""Views for blog app."""
from django.views.generic import TemplateView, CreateView, UpdateView
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from blog.models import Entry, Album
from blog.forms import EntryForm, AlbumForm
from django.urls import reverse_lazy


class EntryView(TemplateView):
	"""A class based view for Multiple Entries."""

	template_name = "blog/entry.html"

	def get_context_data(self):
		"""Extending get_context_data method to add data."""
		entries = Entry.objects.filter(published='public').all()
		return {'entries': entries}


class AlbumView(TemplateView):
	"""Class based view for Album view."""

	template_name = "blog/albums.html"

	def get_context_data(self):
		"""Extending get_context_data method."""
		albums = Album.objects.filter(published='public').all()
		return {'albums': albums}


class EntryIdView(TemplateView):
	"""Class based view for individual entry view."""

	template_name = "blog/entry_id.html"

	def get_context_data(self, pk):
		"""Extending get_context_data method for our data."""
		entry = Entry.objects.get(pk=pk)
		if entry.published == 'public' or entry.author.user == self.request.user:
			return {"entry": entry}
		else:
			error = "I'm sorry, that entry is not available."
			return {"error": error}


class AlbumIdView(TemplateView):
	"""A class based view for individual album view."""

	template_name = "blog/album_id.html"

	def get_context_data(self, pk):
		"""Extend get_context_data method for our data to render."""
		album = Album.objects.get(pk=pk)
		if album.published == 'public' or album.owner.user == self.request.user:
			entry = album.entries.all()
			return {"album": album, "entry": entry}
		else:
			error = "I'm sorry, that album is not available."
			return {"error": error}


class AddEntryView(LoginRequiredMixin, CreateView):
	"""A class based view to add an entry."""

	model = Entry
	form_class = EntryForm
	template_name = 'blog/add_entry.html'
	login_url = reverse_lazy("login")

	def form_valid(self, form):
		"""Execute if form is valid."""
		entry = form.save()
		entry.author = self.request.user.profile
		entry.date_uploaded = timezone.now()
		entry.date_modified = timezone.now()
		if entry.published == "public":
			entry.published_date = timezone.now()
		entry.save()
		return redirect('entries')


class AddAlbumView(LoginRequiredMixin, CreateView):
	"""A class based view to add an Album."""

	model = Album
	form_class = AlbumForm
	template_name = 'blog/add_album.html'
	login_url = reverse_lazy("login")

	def form_valid(self, form):
		"""Execute if form is valid."""
		album = form.save()
		album.owner = self.request.user.profile
		album.date_created = timezone.now()
		album.save()
		return redirect('entries')


class EntryEditView(LoginRequiredMixin, UpdateView):
	"""A class based view to edit an entry."""

	model = Entry
	form_class = EntryForm
	template_name = 'blog/add_entry.html'
	login_url = reverse_lazy("login")

	def form_valid(self, form):
		"""Execute if form is valid."""
		entry = form.save()
		entry.date_modified = timezone.now()
		if entry.published == "public":
			entry.published_date = timezone.now()
		entry.save()
		return redirect('entries')


class AlbumEditView(LoginRequiredMixin, UpdateView):
	"""A class based view to edit an album."""

	model = Album
	form_class = AlbumForm
	template_name = 'blog/add_album.html'
	login_url = reverse_lazy("login")

	def form_valid(self, form):
		"""Execute if form is valid."""
		album = form.save()
		album.date_modified = timezone.now()
		if album.published == "public":
			album.published_date = timezone.now()
		album.save()
		return redirect('entries')
"""Forms."""

from django import forms
from blog.models import Entry, Album


class EntryForm(forms.ModelForm):
    """This makes a form."""

    class Meta:
        model = Entry
        exclude = ['author', 'date_modified', 'date_published', 'date_uploaded']


class AlbumForm(forms.ModelForm):
    """This makes a form."""

    class Meta:
        model = Album
        exclude = ['owner', 'date_modified', 'date_published', 'date_created']
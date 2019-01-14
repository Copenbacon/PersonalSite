"""Blog URL Configuration."""

from django.conf.urls import url
from blog.views import EntryView, AlbumView, \
    EntryIdView, AlbumIdView, AddEntryView, AddAlbumView, EntryEditView, AlbumEditView, FitnessEntryView, MaintenanceEntryView, RecipeEntryView

urlpatterns = [
    url(r'^entries/$', EntryView.as_view(), name="entries"),
    url(r'^fitness/entries/$', FitnessEntryView.as_view(), name="fitness_entries"),
    url(r'^maintenance/entries/$', MaintenanceEntryView.as_view(), name="maintenance_entries"),
    url(r'^recipes/entries/$', RecipeEntryView.as_view(), name="recipe_entries"),
    url(r'^albums/$', AlbumView.as_view(), name="albums"),
    url(r'^entries/(?P<pk>\d+)/$', EntryIdView.as_view(), name="individual_entry"),
    url(r'^albums/(?P<pk>\d+)/$', AlbumIdView.as_view(), name="individual_album"),
    url(r'^albums/add/$', AddAlbumView.as_view(), name="add_albums"),
    url(r'^entries/add/$', AddEntryView.as_view(), name="add_entries"),
    url(r'^entries/(?P<pk>\d+)/edit/$', EntryEditView.as_view(), name="edit_entry"),
    url(r'^albums/(?P<pk>\d+)/edit/$', AlbumEditView.as_view(), name="edit_album"),
]

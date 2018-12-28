"""Views for Home Page."""
from django.conf import settings
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render


def HomeView(request):
    """A class based view for home page."""

    return render(request, "home.html")

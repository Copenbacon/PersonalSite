"""Test the Entry and Entry Album Models."""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Entry, Album
import factory


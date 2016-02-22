from django.db import models
from django.contrib.auth.models import User


class Tracker(models.Model):
    """ Represents an instance of a Tracker """
    user = models.ForeignKey(User, related_name="trackers")
    title = models.CharField(max_length=256)
    snippet = models.CharField(max_length=256, default="JS Snippet")

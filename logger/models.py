from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField


class Tracker(models.Model):
    """
    Represents an instance of a Tracker
    """
    user = models.ForeignKey(User, related_name="trackers")
    title = models.CharField(max_length=256)
    snippet = models.CharField(max_length=256, default="JS Snippet")


class PageLoad(models.Model):
    """
    Represents the Loads of a page by a single user
    saved in a session
    """
    tracker = models.ForeignKey(Tracker)
    user_id = UUIDField(auto=True, unique=True)
    loads = models.IntegerField(default=1)

from django.db import models
from django.contrib.auth.models import User
import uuid


class Tracker(models.Model):
    """
    Represents an instance of a Tracker
    """
    user = models.ForeignKey(User, related_name="trackers")
    title = models.CharField(max_length=256)
    snippet = models.CharField(max_length=256, default="JS Snippet")

    def total_page_loads(self):
        """
        returns number of page loads for a Tracker
        """
        return self.page_loads.aggregate(models.Sum('loads'))["loads__sum"]

    def total_mouse_clicks(self):
        """
        returns total number of clicks for a page
        """
        return self.mouse_clicks.aggregate(models.Sum('clicks'))["clicks__sum"]


class TrackedUser (models.Model):
    """
    A Single TrackedUser Entry where id is saved in Session
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tracker = models.ForeignKey(Tracker)
    created_at = models.DateTimeField(auto_now_add=True)


class PageLoad(models.Model):
    """
    Represents the Loads of a page by a single user
    saved in a session
    """
    tracker = models.ForeignKey(Tracker, related_name="page_loads")
    # user_id = UUIDField(auto=True, unique=True)
    user_id = models.UUIDField(default=uuid.uuid4)
    loads = models.IntegerField(default=1)

    class Meta:
        unique_together = ('tracker', 'user_id')


class MouseClick(models.Model):
    """
    Represents clicks of a single user on a page
    """
    tracker = models.ForeignKey(Tracker, related_name="mouse_clicks")
    user_id = models.UUIDField(default=uuid.uuid4)
    clicks = models.IntegerField(default=1)

    class Meta:
        unique_together = ('tracker', 'user_id')

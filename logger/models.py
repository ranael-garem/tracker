import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tracker(models.Model):
    """
    Represents an instance of a Tracker
    """
    user = models.ForeignKey(User, related_name="trackers")
    title = models.CharField(max_length=256)
    snippet = models.CharField(max_length=1024)
    url = models.URLField(max_length=256)

    def __unicode__(self):
        return self.title


class TrackedUser (models.Model):
    """
    A Single TrackedUser Entry where id is saved in Session
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tracker = models.ForeignKey(Tracker)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "ID: %s \n Tracker: %s \n created_at: %s" % (
            self.id, self.tracker, self.created_at)


class Session(models.Model):
    """
    Represents TrackedUser Session (tracks user activities)
    """
    tracker = models.ForeignKey(Tracker, related_name="sessions")
    user_id = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(minutes=30))
    country_code = models.CharField(max_length=128, default="Unknown")
    country_name = models.CharField(max_length=128, default="Not Set") 

    def __unicode__(self):
        return str(self.id)

    def total_page_loads(self):
        """
        returns number of page loads for a User's Session
        """
        return self.page_loads.count()

    def total_mouse_clicks(self):
        """
        returns total number of clicks for a User's Session
        """
        return self.mouse_clicks.count()


class Page(models.Model):
    """
    Represents a page of website being tracked
    """
    tracker = models.ForeignKey(Tracker, related_name="pages")
    path_name = models.CharField(max_length=128, unique=True)
    height = models.IntegerField(default=700)
    href = models.CharField(max_length=256)

    def __unicode__(self):
        return self.href


class PageLoad(models.Model):
    """
    Represents the Loads of a page by a single user
    saved in a session
    """
    session = models.ForeignKey(Session, related_name="page_loads")
    user_id = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        Page, null=True, blank=True, related_name="page_loads")

    scroll_height = models.IntegerField(default=0)

    def __unicode__(self):
        return "Session: %s \n User_Id: %s \n Created_at: %s, Page:%s" % (
            self.session.id, self.user_id, self.created_at, self.page)


class MouseClick(models.Model):
    """
    Represents clicks of a single user on a page
    """
    session = models.ForeignKey(Session, related_name="mouse_clicks")
    user_id = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        Page, null=True, blank=True, related_name="mouse_clicks")
    x = models.IntegerField()
    y = models.IntegerField()

    def __unicode__(self):
        return "Session: %s \n Created_at: %s" % (
            self.session, self.created_at)


class MouseMove(models.Model):
    """
    Represents mouse move of a single user on a page
    """
    session = models.ForeignKey(Session, related_name="mouse_moves")
    user_id = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        Page, null=True, blank=True, related_name="mouse_moves")
    coordinates = models.CharField(max_length=1024)

    def __unicode__(self):
        return "Session: %s \n Created_at: %s" % (
            self.session, self.created_at)

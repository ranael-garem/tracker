import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User


class Tracker(models.Model):
    """
    Represents an instance of a Tracker
    """
    user = models.ForeignKey(User, related_name="trackers")
    title = models.CharField(max_length=256)
    snippet = models.CharField(max_length=256, default="JS Snippet")

    def __unicode__(self):
        return self.title

    def total_page_loads(self):
        """
        returns number of page loads for a Tracker
        """
        return self.page_loads.count()

    def total_mouse_clicks(self):
        """
        returns total number of clicks for a page
        """
        return self.mouse_clicks.count()


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
        default=datetime.datetime.now + datetime.timedelta(minutes=30))

    def __unicode__(self):
        return "TRACKER: %s, USER: %s, created_at: %s, expiry_date: %s " % (
            self.tracker, self.user_id, self.created_at, self.expiry_date)


class PageLoad(models.Model):
    """
    Represents the Loads of a page by a single user
    saved in a session
    """
    session = models.ForeignKey(Session, related_name="page_loads")
    user_id = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return "Session: %s \n User_Id: %s \n Created_at: %s, Page: %s" % (
            self.session, self.user_id, self.created_at, self.page)


class MouseClick(models.Model):
    """
    Represents clicks of a single user on a page
    """
    session = models.ForeignKey(Session, related_name="mouse_clicks")
    user_id = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return "Session: %s \n User_Id: %s \n Created_at: %s, Page: %s" % (
            self.session, self.user_id, self.created_at, self.page)

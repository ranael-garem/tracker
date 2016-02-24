from rest_framework import permissions
from .models import Tracker


class IsCurrentUser(permissions.BasePermission):
    """
    Allows a User to only change his/her info
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj == request.user


class OnlyAllow10Trackers(permissions.BasePermission):
    """
    Allows Only 10 instances of Tracker for each user
    """

    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        elif request.user.is_authenticated():
            return Tracker.objects.filter(
                user=request.user).count() < 10

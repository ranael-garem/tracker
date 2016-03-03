from rest_framework import permissions
from .models import Tracker


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


class OnlyAllowSafeMethods(permissions.BasePermission):
    """
    Only allows Safe Methods eg: GET
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

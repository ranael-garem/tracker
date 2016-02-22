from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):
    """ Allows a User to only change his/her info """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj == request.user

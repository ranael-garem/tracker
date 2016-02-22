from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from . import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions.IsCurrentUser,

from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, TrackerSerializer
from . import permissions
from .models import Tracker


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions.IsCurrentUser,


class TrackerViewSet(viewsets.ModelViewSet):
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

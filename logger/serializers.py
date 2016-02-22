from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class TrackerSerializer(serializers.HyperlinkedModelSerializer):
    snippet = serializers.CharField(read_only=True)

    class Meta:
        model = models.Tracker
        fields = ('url', 'title', 'snippet')

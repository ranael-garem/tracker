from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class PageLoadSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()

    class Meta:
        model = models.PageLoad
        fields = ('user_id', 'loads', 'tracker')


class TrackerSerializer(serializers.HyperlinkedModelSerializer):
    page_loads = PageLoadSerializer(many=True, read_only=True)
    snippet = serializers.CharField(read_only=True)

    class Meta:
        model = models.Tracker
        fields = ('url', 'title', 'snippet', 'page_loads', 'total_page_loads')

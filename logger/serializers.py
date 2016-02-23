from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class PageLoadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PageLoad
        fields = ('id', 'user_id', 'loads')


class TrackerSerializer(serializers.HyperlinkedModelSerializer):
    # page_loads = PageLoadSerializer(many=True)
    snippet = serializers.CharField(read_only=True)

    class Meta:
        model = models.Tracker
        fields = ('url', 'title', 'snippet', 'total_page_loads')

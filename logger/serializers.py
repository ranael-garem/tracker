from rest_framework import serializers
from . import models


class TrackedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrackedUser
        fields = ('id', 'tracker', 'created_at')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ('__all__')


class PageLoadSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()

    class Meta:
        model = models.PageLoad
        fields = ('user_id', 'session', 'created_at')


class MouseClickSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()

    class Meta:
        model = models.PageLoad
        fields = ('user_id', 'session', 'created_at')


class TrackerSerializer(serializers.HyperlinkedModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)
    snippet = serializers.CharField(read_only=True)

    class Meta:
        model = models.Tracker
        fields = ('url', 'id', 'title', 'snippet', 'sessions')

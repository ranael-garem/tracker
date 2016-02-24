from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, TrackerSerializer, PageLoadSerializer
from . import permissions
from .models import Tracker, PageLoad


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions.IsCurrentUser,


class TrackerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows current user's trackers to be viewed or edited.
    """
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer
    permission_classes = permissions.OnlyAllow10Trackers,

    def get_queryset(self):
        """
        returns User's trackers for authenticated users
        """
        if self.request.user.is_authenticated():
            return Tracker.objects.filter(user=self.request.user)
        else:
            return None

    def perform_create(self, serializer):
        """
        Assigns current user to Tracker instance
        """
        return serializer.save(user=self.request.user)


class PageLoadView(APIView):
    """
    Creates or increments 'loads' of PageLoad Object
    for the current user saved in the SESSION
    """

    def get(self, request, pk, format=None):
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            (page_load, created) = PageLoad.objects.get_or_create(
                user_id=user_id, tracker_id=pk)
            if not created:
                page_load.loads += 1
                page_load.save()
        else:
            page_load = PageLoad.objects.create(tracker_id=pk)
            serializer = PageLoadSerializer(page_load)
            request.session['user_id'] = serializer.data['user_id']
        return Response({'user_id': request.session['user_id']})


class UserIdView(APIView):
    """
    Returns the user_id if saved in current session
    For Testing Purposes Only
    """

    def get(self, request, format=None):
        if 'user_id' in request.session:
            return Response({'user_id': request.session['user_id']})
        else:
            return Response()


class ClearSessionView(APIView):
    """
    View responsible for clearing the current session
    For Testing Purposes Only
    """
    def get(self, request, format=None):
        try:
            del request.session['user_id']
        except KeyError:
            pass
        return Response("SESSION CLEARED")

import datetime
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    TrackerSerializer, TrackedUserSerializer)
from . import permissions
from .models import (
    MouseClick, PageLoad, Tracker,
    TrackedUser, Session)


class APIRoot(APIView):
    def get(self, request):
        return Response({
            'users': reverse('user-list', request=request),
            'trackers': reverse('tracker-list', request=request),
            'tracked_users': reverse('trackeduser-list', request=request),
            'clear_session': reverse('clear', request=request),
            'current_user_id': reverse('user-id', request=request),

        })


class TrackedUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    # TODO Change to ListApiView
    """
    queryset = TrackedUser.objects.all()
    serializer_class = TrackedUserSerializer
    permission_classes = permissions.OnlyAllowSafeMethods,


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
    Creates a PageLoad Object for the current user saved/created in the SESSION
    # TODO: page field
    """

    def get(self, request, pk, path, format=None):
        if 'user_id' in request.session:
            user_id = request.session['user_id']
        else:
            user_id = TrackedUserSerializer(
                TrackedUser.objects.create(tracker_id=pk)).data['id']
            request.session['user_id'] = user_id

        if 'session_id' in request.session:
            user_session = Session.objects.get(
                id=request.session['session_id'])
            if user_session.expiry_date < timezone.now():
                print "EXPIRED"
                del request.session['session_id']
                user_session = Session.objects.create(
                    tracker_id=pk, user_id=user_id)
                request.session['session_id'] = user_session.id
            else:
                print "UPDATE_EXPIRY_DATE"
                user_session.expiry_date = timezone.now(
                ) + datetime.timedelta(minutes=30)
                user_session.save()

        else:
            print 'USER', user_id
            user_session = Session.objects.create(
                tracker_id=pk, user_id=user_id)
            request.session['session_id'] = user_session.id

        PageLoad.objects.create(
            session=user_session, user_id=user_id, page=path)

        return Response({'user_id': request.session['user_id'],
                         'session_id': request.session['session_id']},
                        )


class MouseClickView(APIView):
    """
    Creates a MouseClick Object for the current user
    saved/created in the SESSION
    # TODO: page field
    """

    def get(self, request, pk, path, format=None):
        if 'user_id' in request.session:
            user_id = request.session['user_id']
        else:
            user_id = TrackedUserSerializer(
                TrackedUser.objects.create(tracker_id=pk)).data['id']
            request.session['user_id'] = user_id

        if 'session_id' in request.session:
            user_session = Session.objects.get(
                id=request.session['session_id'])
            if user_session.expiry_date < timezone.now():
                print "EXPIRED"
                del request.session['session_id']
                user_session = Session.objects.create(
                    tracker_id=pk, user_id=user_id)
                request.session['session_id'] = user_session.id
            else:
                print "UPDATE_EXPIRY_DATE"
                user_session.expiry_date = timezone.now(
                ) + datetime.timedelta(minutes=30)
                user_session.save()

        else:
            print 'USER', user_id
            user_session = Session.objects.create(
                tracker_id=pk, user_id=user_id)
            request.session['session_id'] = user_session.id

        MouseClick.objects.create(
            session=user_session, user_id=user_id, page=path)

        return Response({'user_id': request.session['user_id'],
                         'session_id': request.session['session_id']},
                        )


class UserIdSessionIdView(APIView):
    """
    Returns the user_id and session_id if saved in current session
    For Testing Purposes Only
    """

    def get(self, request, format=None):
        context = {}

        if 'user_id' in request.session:
            context.update({'user_id': request.session['user_id']})
        if 'session_id' in request.session:
            context.update({'session_id': request.session['session_id']})

        return Response(context)


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
        try:
            del request.session['session_id']
        except KeyError:
            pass
        return Response("SESSION CLEARED")

import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer, TrackerSerializer, TrackedUserSerializer)
from . import permissions
from .models import Tracker, TrackedUser, PageLoad, MouseClick
from .helpers import percentage_increase


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions.IsCurrentUser,


class TrackedUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    #TODO Change to ListApiView
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
    Creates a PageLoad Object for the current user saved/creates in the SESSION
    """

    def get(self, request, pk, format=None):
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            PageLoad.objects.create(
                user_id=user_id, tracker_id=pk)

        else:
            tracked_user = TrackedUser.objects.create(tracker_id=pk)
            PageLoad.objects.create(
                tracker_id=pk, user_id=tracked_user.id)
            serializer = TrackedUserSerializer(tracked_user)
            request.session['user_id'] = serializer.data['id']
        return Response({'user_id': request.session['user_id']})


class MouseClickView(APIView):
    """
    Creates a MouseClick Object for the current user
    saved/created in the SESSION
    """

    def get(self, request, pk, format=None):
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            MouseClick.objects.create(user_id=user_id, tracker_id=pk)

        else:
            tracked_user = TrackedUser.objects.create(tracker_id=pk)
            MouseClick.objects.create(tracker_id=pk, user_id=tracked_user.id)
            serializer = TrackedUserSerializer(tracked_user)
            request.session['user_id'] = serializer.data['id']
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


class PopularityView(APIView):
    """
    Calculates the Popularity Increase% in the last day, last week, last month
    and if given a specified from/to date. \n
    Calculation is based on the number of new users
    """

    def get(self, request, pk,
            FY=None, FM=None, FD=None,
            TY=None, TM=None, TD=None, format=None):
        all_users = TrackedUser.objects.filter(tracker=pk).count()

        last_day_users = TrackedUser.objects.filter(tracker=pk).exclude(
            created_at__gte=datetime.datetime.now().date()).count()

        last_week_users = TrackedUser.objects.filter(tracker=pk).exclude(
            created_at__gte=((datetime.datetime.now().date() -
                              datetime.timedelta(days=7)))).count()

        last_month_users = TrackedUser.objects.filter(tracker=pk).exclude(
            created_at__gte=((datetime.datetime.now().date() -
                              datetime.timedelta(days=30)))).count()

        in_the_last_day = percentage_increase(last_day_users, all_users)
        in_the_last_week = percentage_increase(last_week_users, all_users)
        in_the_last_month = percentage_increase(last_month_users, all_users)

        if FM and FM and FD and TY and TM and TD:
            from_users = TrackedUser.objects.filter(tracker=pk).exclude(
                created_at__gte=datetime.date(
                    int(FY), int(FM), int(FD)) + datetime.timedelta(days=1)
            ).count()
            to_users = TrackedUser.objects.filter(tracker=pk).exclude(
                created_at__gte=datetime.date(
                    int(TY), int(TM), int(TD)) + datetime.timedelta(days=1)
            ).count()
            from_to = percentage_increase(from_users, to_users)
        else:
            from_to = None

        return Response({
            'in_last_day': in_the_last_day,
            'in_last_week': in_the_last_week,
            'in_last_month': in_the_last_month,
            'popularity_increase_from_to': from_to

        })


class InteractivityView(APIView):

    def get(self, request, pk, format=None):
        tracker = Tracker.objects.get(id=pk)
        avg_clicks = float(tracker.total_mouse_clicks()) / \
            float(tracker.total_page_loads())
        return Response({
            "avg_clicks": avg_clicks,
        })

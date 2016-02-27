import datetime
from django.utils import timezone
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer, TrackerSerializer, TrackedUserSerializer)
from . import permissions
from .models import (
    MouseClick, PageLoad, Tracker,
    TrackedUser, Session)
from .helpers import percentage_increase


class APIRoot(APIView):
    def get(self, request):
        return Response({
            'users': reverse('user-list', request=request),
            'trackers': reverse('tracker-list', request=request),
            'tracked_users': reverse('trackeduser-list', request=request),
            'clear_session': reverse('clear', request=request),
            'current_user_id': reverse('user-id', request=request),

        })


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
    Creates a PageLoad Object for the current user saved/created in the SESSION
    # TODO: page field
    """

    def get(self, request, pk, format=None):
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
                user_session.expiry_date += datetime.timedelta(minutes=30)
                user_session.save()

        else:
            print 'USER', user_id
            user_session = Session.objects.create(
                tracker_id=pk, user_id=user_id)
            request.session['session_id'] = user_session.id

        PageLoad.objects.create(session=user_session, user_id=user_id)

        return Response({'user_id': request.session['user_id'],
                         'session_id': request.session['session_id']},
                        )


class MouseClickView(APIView):
    """
    Creates a MouseClick Object for the current user
    saved/created in the SESSION
    # TODO: page field
    """

    def get(self, request, pk, format=None):
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
                user_session.expiry_date += datetime.timedelta(minutes=30)
                user_session.save()

        else:
            print 'USER', user_id
            user_session = Session.objects.create(
                tracker_id=pk, user_id=user_id)
            request.session['session_id'] = user_session.id

        MouseClick.objects.create(session=user_session, user_id=user_id)

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

        [in_the_last_day, in_the_last_week,
            in_the_last_month] = self.calculate_popularity(pk)

        if FM and FM and FD and TY and TM and TD:
            from_to = self.calculate_popularity_from_to(
                pk,
                datetime.date(int(FY), int(FM), int(FD)),
                datetime.date(int(TY), int(TM), int(TD)))
        else:
            from_to = None

        return Response({
            'in_last_day': in_the_last_day,
            'in_last_week': in_the_last_week,
            'in_last_month': in_the_last_month,
            'popularity_increase_from_to': from_to

        })

    def calculate_popularity(self, tracker_id):
        """
        Calcualtes popularity increase in the last day, week, month
        """
        all_users = TrackedUser.objects.filter(tracker=tracker_id).count()

        last_day_users = TrackedUser.objects.filter(
            tracker=tracker_id,
            created_at__lt=datetime.datetime.now().date()).count()

        last_week_users = TrackedUser.objects.filter(
            tracker=tracker_id,
            created_at__lt=((datetime.datetime.now().date() -
                             datetime.timedelta(days=7)))).count()

        last_month_users = TrackedUser.objects.filter(
            tracker=tracker_id,
            created_at__lt=((datetime.datetime.now().date() -
                             datetime.timedelta(days=30)))).count()

        in_the_last_day = percentage_increase(last_day_users, all_users)
        in_the_last_week = percentage_increase(last_week_users, all_users)
        in_the_last_month = percentage_increase(last_month_users, all_users)

        return [in_the_last_day, in_the_last_week, in_the_last_month]

    def calculate_popularity_from_to(self, tracker_id, from_date, to_date):
        """
        Calculates popularity increase given a from_date and to_date
        """
        from_users = TrackedUser.objects.filter(tracker=tracker_id).exclude(
            created_at__gte=from_date + datetime.timedelta(days=1)).count()

        to_users = TrackedUser.objects.filter(tracker=tracker_id).exclude(
            created_at__gte=to_date + datetime.timedelta(days=1)
        ).count()
        return percentage_increase(from_users, to_users)


class InteractivityView(APIView):
    """
    Calculates average interactivity, interactivity in the current day, and
    interactivity in each day specified in a given time range (From/To date)
    """

    def get(self, request, pk,
            FY=None, FM=None, FD=None,
            TY=None, TM=None, TD=None, format=None):

        [avg_clicks, avg_today] = self.calculate_interactivity(pk)

        if FM and FM and FD and TY and TM and TD:
            from_date = datetime.date(int(FY), int(FM), int(FD))
            to_date = datetime.date(int(TY), int(TM), int(TD))
            from_to_values = self.calculate_interactivity_from_to(
                pk, from_date, to_date)
        else:
            from_to_values = []

        return Response({
            "avg_clicks": avg_clicks,
            "avg_today": avg_today,
            "from_to_values": from_to_values,
        })

    def calculate_interactivity(self, tracker_id):
        """
        Calculates average all time interactivity, and in the current day
        """
        page_loads = Session.objects.filter(tracker_id=tracker_id).annotate(
            loads=Count('page_loads')).aggregate(Sum('loads'))['loads__sum']
        mouse_clicks = Session.objects.filter(tracker_id=tracker_id).annotate(
            clicks=Count('mouse_clicks')).aggregate(
            Sum('clicks'))['clicks__sum']
        avg_clicks = float(page_loads) / float(mouse_clicks)

        sessions = Tracker.objects.get(id=tracker_id).sessions.values('id')
        today_loads = PageLoad.objects.filter(
            session__in=sessions,
            created_at__gte=datetime.datetime.now().date()).count()
        today_clicks = MouseClick.objects.filter(
            session__in=sessions,
            created_at__gte=datetime.datetime.now().date()).count()
        if today_loads != 0:
            avg_today = float(today_clicks) / float(today_loads)
        else:
            avg_today = None

        return [avg_clicks, avg_today]

    def calculate_interactivity_from_to(self, tracker_id, from_date, to_date):
        """
        Calculates Interactivity for each day in the timerange specified
        (From/To date)
        Returns list of [day, interactivity value]
        """
        list = []
        sessions = Tracker.objects.get(id=tracker_id).sessions.values('id')
        delta = datetime.timedelta(days=1)
        while from_date <= to_date:
            loads = PageLoad.objects.filter(
                session__in=sessions,
                created_at__year=from_date.year,
                created_at__month=from_date.month,
                created_at__day=from_date.day).count()
            clicks = MouseClick.objects.filter(
                session__in=sessions,
                created_at__year=from_date.year,
                created_at__month=from_date.month,
                created_at__day=from_date.day).count()
            if loads != 0:
                list.append([from_date, float(clicks) / float(loads)])
            else:
                list.append([from_date, None])
            from_date += delta

        return list

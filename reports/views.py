import datetime
from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from logger.models import (
    MouseClick, PageLoad, Tracker,
    TrackedUser, Session)
from .helpers import percentage_increase


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

        users = TrackedUser.objects.filter(tracker=pk).count()
        today_users = TrackedUser.objects.filter(
            tracker=pk,
            created_at__gte=datetime.datetime.now().date()).count()
        visits = Session.objects.filter(tracker=pk).count()

        return Response({
            'in_last_day': in_the_last_day,
            'in_last_week': in_the_last_week,
            'in_last_month': in_the_last_month,
            'popularity_increase_from_to': from_to,
            'users': users,
            'today_users': today_users,
            'visits': visits,

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

        avg_clicks = round(float(mouse_clicks) / float(page_loads), 2)

        sessions = Tracker.objects.get(id=tracker_id).sessions.values('id')
        today_loads = PageLoad.objects.filter(
            session__in=sessions,
            created_at__gte=datetime.datetime.now().date()).count()
        today_clicks = MouseClick.objects.filter(
            session__in=sessions,
            created_at__gte=datetime.datetime.now().date()).count()
        if today_loads != 0:
            avg_today = round(float(today_clicks) / float(today_loads), 2)
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


class VisitsOverTime(APIView):
    """
    Returns number of visits for each day in a time interval
    """

    def get(self, request, pk,
            FY=None, FM=None, FD=None,
            TY=None, TM=None, TD=None, format=None):
        labels = []
        data = []
        if FM and FM and FD and TY and TM and TD:
            from_date = datetime.date(int(FY), int(FM), int(FD))
            to_date = datetime.date(int(TY), int(TM), int(TD))
        else:
            to_date = datetime.datetime.now().date()
            from_date = to_date - datetime.timedelta(days=15)

        while from_date <= to_date:
            visits = Session.objects.filter(tracker=pk,
                                            created_at__year=from_date.year,
                                            created_at__month=from_date.month,
                                            created_at__day=from_date.day
                                            ).count()
            labels.append(
                "" + from_date.strftime('%b') + " " + str(from_date.day))
            data.append(visits)
            from_date += datetime.timedelta(days=1)
        return Response({"labels": labels,
                         "values": data})


class NewUsersView(APIView):
    """
    Returns number of new users for each day in a time interval
    """

    def get(self, request, pk,
            FY=None, FM=None, FD=None,
            TY=None, TM=None, TD=None, format=None):
        labels = []
        data = []
        if FM and FM and FD and TY and TM and TD:
            from_date = datetime.date(int(FY), int(FM), int(FD))
            to_date = datetime.date(int(TY), int(TM), int(TD))
        else:
            to_date = datetime.datetime.now().date()
            from_date = to_date - datetime.timedelta(days=15)

        while from_date <= to_date:
            visits = TrackedUser.objects.filter(
                tracker=pk,
                created_at__year=from_date.year,
                created_at__month=from_date.month,
                created_at__day=from_date.day
            ).count()
            labels.append(
                "" + from_date.strftime('%b') + " " + str(from_date.day))
            data.append(visits)
            from_date += datetime.timedelta(days=1)
        return Response({"labels": labels,
                         "values": data})

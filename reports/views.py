import datetime
from time import time
from itertools import chain

from django.db.models import Count, Sum
from django.views.generic import TemplateView
from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework.response import Response

from logger.models import (
    MouseClick, PageLoad, Page, Tracker,
    TrackedUser, Session, MouseMove)
from .helpers import percentage_increase
from reports.models import ScreenShot


class PopularityView(APIView):
    """
    Calculates the Popularity Increase% in the last day, last week, last month
    and if given a specified from/to date. \n
    Calculation is based on the number of new users
    """

    def get(self, request, pk,
            FY=None, FM=None, FD=None,
            TY=None, TM=None, TD=None, format=None):

        [in_the_last_day, in_the_last_week, last_week_class,
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
        last_week_percentage = percentage_increase(last_week_users, all_users)
        in_the_last_month = percentage_increase(last_month_users, all_users)

        if int(in_the_last_day[:-1]) < 0:
            last_week_class = "red"
            last_week_sort = "desc"
        else:
            last_week_class = "green"
            last_week_sort = "asc"

        in_the_last_week = [
            last_week_percentage, last_week_class, last_week_sort]
        return [in_the_last_day, in_the_last_week,
                last_week_class, in_the_last_month]

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


class BounceRateView(APIView):
    """
    Returns bounce rate for each day in a time interval
    and total bounce rate
    """

    def get(self, request, pk,
            FY=None, FM=None, FD=None,
            TY=None, TM=None, TD=None, format=None):
        labels = []
        data = []
        all_visits = Session.objects.filter(tracker_id=pk)
        visits_with_one_page_view = all_visits.annotate(
            num_pages=Count('page_loads__page',
                            distinct=True)).filter(num_pages=1).count()
        if all_visits.count() != 0:
            avg_bounce_rate = round((
                float(visits_with_one_page_view) /
                float(all_visits.count())) * 100, 1)
        else:
            avg_bounce_rate = None

        if FM and FM and FD and TY and TM and TD:
            from_date = datetime.date(int(FY), int(FM), int(FD))
            to_date = datetime.date(int(TY), int(TM), int(TD))
        else:
            to_date = datetime.datetime.now().date()
            from_date = to_date - datetime.timedelta(days=15)

        while from_date <= to_date:
            all_visits = Session.objects.filter(
                tracker_id=pk,
                created_at__year=from_date.year,
                created_at__month=from_date.month,
                created_at__day=from_date.day
            )
            visits_with_one_page_view = all_visits.annotate(
                num_pages=Count('page_loads__page',
                                distinct=True)).filter(num_pages=1).count()

            if all_visits.count() != 0:
                bounce_rate = round((float(visits_with_one_page_view) /
                                     float(all_visits.count())) * 100, 2)
            else:
                bounce_rate = None
            labels.append(
                "" + from_date.strftime('%b') + " " + str(from_date.day))
            data.append(bounce_rate)
            from_date += datetime.timedelta(days=1)

        return Response({"bounce_rate": avg_bounce_rate,
                         "labels": labels,
                         "values": data})


class HeatMapView(APIView):
    """
    Returns X and Y coordinates of mouseclicks of a given page for
    a ClickHeatMap
    """

    def get(self, request, page_id, format=None):
        try:
            page = Page.objects.get(id=page_id)
            tracker = Tracker.objects.get(id=page.tracker_id)
            sessions = tracker.sessions.values('id')
            clicks = MouseClick.objects.filter(
                session__in=sessions, page=page).values_list('y', 'x')
            return Response({"clicks": clicks,
                            "url": tracker.url,
                            "path_name": page.path_name,
                            "page_height": page.height})
        except:
            return Response("Page id is incorrect")


class CountriesView(APIView):
    """
    Returns number of visits for each country
    """

    def get(self, request, pk,
            FY=None, FM=None, FD=None,
            TY=None, TM=None, TD=None, format=None):
        if FM and FM and FD and TY and TM and TD:
            from_date = datetime.date(int(FY), int(FM), int(FD))
            to_date = datetime.date(
                int(TY), int(TM), int(TD) +
                datetime.timedelta(days=1))
        else:
            to_date = datetime.datetime.now().date() + \
                datetime.timedelta(days=1)
            from_date = to_date - datetime.timedelta(days=14)

        all_visits = Session.objects.filter(
            tracker_id=pk,
            created_at__lte=to_date,
            created_at__gte=from_date,
        )
        return Response({
            all_visits.values("country_code").annotate(visits=Count("pk"))})


class IframeView(TemplateView):
    """
    View responsible for rendering an iframe
    """
    template_name = "iframe.html"

    def get_context_data(self, **kwargs):
        context = super(IframeView, self).get_context_data(**kwargs)
        context['url'] = self.kwargs['url']
        return context


class ScreenShotCreateView(APIView):
    """
    View responsible for creating a Screenshot object
    """

    def post(self, request, format=None):
        source = request.data.items()[0][1] + ';' + request.data.items()[1][0]

        source = str(source)
        source = source.replace(" ", "+")

        filename = "screenshot%s.png" % str(time()).replace('.', '_')
        # imgstr = re.search(r'base64,(.*)', source).group(1)
        imgstr = source.partition('base64,')[2]

        if len(imgstr) % 4 != 0:  # check if multiple of 4
            while len(imgstr) % 4 != 0:
                imgstr = imgstr + "="

        decoded_image = imgstr.decode('base64')
        screenshot = ScreenShot()
        screenshot.image = ContentFile(decoded_image, filename)
        screenshot.save()

        return Response({'screenshot_id': screenshot.id})


class ScrollHeatMapCanvasView(TemplateView):
    """
    Shows Scroll Heat map using a screenshot
    """
    template_name = "scroll.html"

    def get_context_data(self, **kwargs):
        context = super(
            ScrollHeatMapCanvasView, self).get_context_data(**kwargs)
        screenshot = ScreenShot.objects.get(id=self.kwargs['screenshot_id'])
        context['screenshot'] = screenshot
        context['tracker_id'] = self.kwargs['pk']
        context['pathname'] = self.kwargs['path']
        print context['tracker_id']

        return context


class ScrollHeightsView(APIView):
    """
    Returns page height and page scroll heights
    """

    def get(self, request, pk, path, format=None):
        sessions = Tracker.objects.get(id=pk).sessions.values('id')
        (page, created) = Page.objects.get_or_create(
            path_name=path, tracker_id=pk)
        page_loads = PageLoad.objects.filter(
            session__in=sessions, page=page).values('scroll_height')

        return Response({'scroll_heights': page_loads,
                         'page_height': page.height})


class SessionReplayView(APIView):
    def get(self, request, pk, format=None):
        session = [Session.objects.get(id=pk)]
        first_page_load = PageLoad.objects.filter(
            session__in=session)[0]
        first_time = first_page_load.created_at

        all_clicks = MouseClick.objects.filter(
            session__in=session)
        mouse_moves = MouseMove.objects.filter(
            session__in=session)

        result_list = sorted(chain(all_clicks, mouse_moves),
            key=lambda instance: instance.created_at)

        list = []
        for object in result_list:
            time = ((object.created_at - first_time).seconds) * 1000
            if isinstance(object, MouseMove):
                list.append(("MouseMove", object.coordinates, object.page.path_name, time))
            else:
                list.append(("MouseClick", object.y, object.x, object.page.path_name, time))

        time = []
        for object in result_list:
            time.append(((object.created_at - first_time).seconds) * 1000)

        clicks = all_clicks.values_list('y', 'x', 'page__path_name')

        return Response({
            'clicks': clicks, 'time': time,
            'height': first_page_load.page.height,
            'moves': list,
            'url': session[0].tracker.url})

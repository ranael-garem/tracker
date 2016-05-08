import datetime
from django.utils import timezone
from django.db.models import Count

from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    TrackerSerializer, TrackedUserSerializer,
    PageSerializer, SessionSerializer)
from . import permissions
from .models import (
    MouseClick, PageLoad, Tracker,
    TrackedUser, Session, Page,
    MouseMove)


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
        Assigns current user to Tracker instance and
        auto generates tracking snippet
        """
        instance = serializer.save(user=self.request.user)
        instance.snippet = "<script> \n (function(t, r, a, c, k){" + \
            "c = t.createElement(r), \n" + \
            "k = t.getElementsByTagName(r)[0]; \n" + \
            "c.async = 1; \n" + "c.src = a; \n" + \
            "k.parentNode.insertBefore(c, k) \n" + \
            "})(document, 'script'," + \
            "'http://tracker.juniorgeorgy.webfactional.com/" + \
            "static/javascripts/transmitter.js?tracker=" + \
            str(instance.pk) + "'); \n" + "</script>"
        instance.save()
        return instance


class TrackerPagesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer

    def get_queryset(self):
        tracker_id = self.kwargs['pk']
        pages = Page.objects.filter(tracker_id=tracker_id).annotate(
            num_loads=Count('page_loads'),
            num_clicks=Count('mouse_clicks')).filter(
            num_loads__gt=2, num_clicks__gt=1)
        return pages


class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SessionSerializer

    def get_queryset(self):
        tracker_id = self.kwargs['pk']
        sessions = Session.objects.filter(
            tracker_id=tracker_id, page_loads__isnull=False).distinct()
        return sessions


class PageLoadView(APIView):
    """
    Creates a PageLoad Object for the current user saved/created in the SESSION
    # TODO: page field
    """

    def get(self, request, pk, height, path, countryName,
            countryCode, city, regionName, ip, lang, href, format=None):
        if 'user_id' in request.session:
            user_id = request.session['user_id']
        else:
            user_id = TrackedUserSerializer(
                TrackedUser.objects.create(tracker_id=pk),
                context={'request': request}).data['id']
            request.session['user_id'] = user_id

        if 'session_id' in request.session:
            user_session = Session.objects.get(
                id=request.session['session_id'])
            print "NOW", timezone.now()
            print "EXP", user_session.expiry_date
            if user_session.expiry_date < timezone.now():
                print "EXPIRED"
                del request.session['session_id']
                user_session = Session.objects.create(
                    tracker_id=pk, user_id=user_id, country_code=countryCode,
                    country_name=countryName)
                print "SESSION ID", user_session.id
                request.session['session_id'] = user_session.id
                print "IN SESSION", request.session['session_id']
            else:
                print "UPDATE_EXPIRY_DATE"
                user_session.expiry_date = timezone.now(
                ) + datetime.timedelta(minutes=30)
                user_session.save()

        else:
            print 'USER', user_id
            user_session = Session.objects.create(
                tracker_id=pk, user_id=user_id, country_code=countryCode,
                country_name=countryName)
            request.session['session_id'] = user_session.id

        if not href.startswith('http://'):
            href = href[:6] + '/' + href[6:]
        if path == 'x':
            path = '/'
        else:
            path = path[1:]
        (page, created) = Page.objects.get_or_create(tracker_id=pk, href=href)
        page.path_name = path
        if page.height != height:
            page.height = height
        page.save()

        page_load = PageLoad.objects.create(
            session=user_session, user_id=user_id, page=page)
        request.session['page_load'] = page_load.id

        return Response({'user_id': request.session['user_id'],
                         'session_id': request.session['session_id']},
                        )


class MouseClickView(APIView):
    """
    Creates a MouseClick Object for the current user
    saved/created in the SESSION
    # TODO: page field
    """

    def get(self, request, pk, x, y, path, href, format=None):
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

        if not href.startswith('http://'):
            href = href[:6] + '/' + href[6:]
        if path == 'x':
            path = '/'
        else:
            path = path[1:]
        (page, created) = Page.objects.get_or_create(tracker_id=pk, href=href)
        page.path_name = path
        page.save()
        MouseClick.objects.create(
            session=user_session, user_id=user_id, page=page, x=x, y=y)

        return Response({'user_id': request.session['user_id'],
                         'session_id': request.session['session_id'], }
                        )


class MouseMoveView(APIView):
    def get(self, request, pk, path, href, coordinates, format=None):
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

        if not href.startswith('http://'):
            href = href[:6] + '/' + href[6:]
        if path == 'x':
            path = '/'
        else:
            path = path[1:]
        (page, created) = Page.objects.get_or_create(
            tracker_id=pk, href=href)
        page.path_name = path
        page.save()
        MouseMove.objects.create(
            session=user_session,
            user_id=user_id, page=page,
            coordinates=coordinates)

        return Response({'user_id': request.session['user_id'],
                         'session_id': request.session['session_id'], }
                        )


class ScrollView(APIView):
    """
    Saves the maximum scroll heigth for a page load
    """

    def get(self, request, scroll, format=None):
        if request.session['page_load']:
            page_load = PageLoad.objects.get(
                id=request.session['page_load'])
            page_load.scroll_height = scroll
            page_load.save()
            return Response(page_load.scroll_height)
        else:
            return Response()


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

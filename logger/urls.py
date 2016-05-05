from django.conf.urls import include, url

from rest_framework import routers

from logger import views as logger_views
from authentication import views as auth_views


router = routers.DefaultRouter()

router.register(r'users', auth_views.UserViewSet)
router.register(r'trackers', logger_views.TrackerViewSet)
router.register(r'tracked_users', logger_views.TrackedUserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/root/$', logger_views.APIRoot.as_view()),

    url(r'^api/trackers/(?P<pk>[0-9]+)/pages/$',
        logger_views.TrackerPagesViewSet.as_view({'get': 'list'})),

    url(r'^api/trackers/(?P<pk>[0-9]+)/sessions/$',
        logger_views.SessionViewSet.as_view({'get': 'list'})),

    url(r'^load/(?P<pk>[0-9]+)/(?P<height>[0-9]+)/(?P<path>.*)/demographics/(?P<countryName>.*)/(?P<countryCode>.*)/(?P<city>.*)/(?P<regionName>.*)/(?P<ip>.*)/(?P<lang>.*)$',
        logger_views.PageLoadView.as_view()),
    url(r'^click/(?P<pk>[0-9]+)/(?P<x>[0-9]+)/(?P<y>[0-9]+)/(?P<path>.*)$',
        logger_views.MouseClickView.as_view()),

    url(r'^mouse/move/(?P<pk>[0-9]+)/(?P<path>.*)$',
        logger_views.MouseMoveView.as_view()),

    url(r'^api/scroll/(?P<scroll>[0-9]+)/', logger_views.ScrollView.as_view()),

    url(r'^user/$', logger_views.UserIdSessionIdView.as_view(),
        name="user-id"),
    url(r'^clear/$', logger_views.ClearSessionView.as_view(), name="clear"),

]

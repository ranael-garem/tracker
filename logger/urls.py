from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from logger import views as logger_views
from authentication import views as auth_views
from tracker.views import IndexView


router = routers.DefaultRouter()

router.register(r'users', auth_views.UserViewSet)
router.register(r'trackers', logger_views.TrackerViewSet)
router.register(r'tracked_users', logger_views.TrackedUserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/root/$', logger_views.APIRoot.as_view()),
    url(r'^api/auth/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^api/auth/logout/$', auth_views.LogoutView.as_view(), name='logout'),


    url(r'^load/(?P<pk>[0-9]+)/$', logger_views.PageLoadView.as_view()),
    url(r'^click/(?P<pk>[0-9]+)/$', logger_views.MouseClickView.as_view()),

    url(r'^user/$', logger_views.UserIdSessionIdView.as_view(),
        name="user-id"),
    url(r'^clear/$', logger_views.ClearSessionView.as_view(), name="clear"),

]

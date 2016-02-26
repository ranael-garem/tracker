from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from logger import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'trackers', views.TrackerViewSet)
router.register(r'tracked_users', views.TrackedUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^load/(?P<pk>[0-9]+)/$', views.PageLoadView.as_view()),
    url(r'^click/(?P<pk>[0-9]+)/$', views.MouseClickView.as_view()),
    url(r'^popularity/(?P<pk>[0-9]+)/$', views.PopularityView.as_view()),
    url(r'^popularity/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        views.PopularityView.as_view()),
    url(r'^interactivity/(?P<pk>[0-9]+)/$', views.InteractivityView.as_view()),
    url(r'^interactivity/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        views.InteractivityView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^test/$', views.UserIdView.as_view()),
    url(r'^clear/$', views.ClearSessionView.as_view()),

]

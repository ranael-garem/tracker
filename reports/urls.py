from django.conf.urls import url

from reports import views as reports_views


urlpatterns = [
    url(r'^popularity/(?P<pk>[0-9]+)/$',
        reports_views.PopularityView.as_view()),
    url(r'^popularity/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        reports_views.PopularityView.as_view()),

    url(r'^interactivity/(?P<pk>[0-9]+)/$',
        reports_views.InteractivityView.as_view()),
    url(r'^interactivity/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        reports_views.InteractivityView.as_view()),

    url(r'^visits/(?P<pk>[0-9]+)/$',
        reports_views.VisitsOverTime.as_view()),
    url(r'^visits/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        reports_views.VisitsOverTime.as_view()),


    url(r'^new-users/(?P<pk>[0-9]+)/$',
        reports_views.NewUsersView.as_view()),
    url(r'^new-users/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        reports_views.NewUsersView.as_view()),

    url(r'^bounce/(?P<pk>[0-9]+)/$',
        reports_views.BounceRateView.as_view()),
    url(r'^bounce/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        reports_views.BounceRateView.as_view()),

    url(r'^heatmap/(?P<pk>[0-9]+)/(?P<path>.*)$',
        reports_views.HeatMapView.as_view()),


    url(r'^countries/(?P<pk>[0-9]+)/$',
        reports_views.CountriesView.as_view()),
    url(r'^countries/(?P<pk>[0-9]+)/(?P<FY>\d{4})/(?P<FM>\d+)/(?P<FD>\d+)/(?P<TY>\d{4})/(?P<TM>\d+)/(?P<TD>\d+)/$',
        reports_views.CountriesView.as_view()),

    url(r'^scroll/heatmap/(?P<url>.*)$', reports_views.IframeView.as_view()),

    url(r'^scroll/heights/(?P<pk>[0-9]+)/(?P<path>.*)$',
        reports_views.ScrollHeightsView.as_view()),

    url(r'^scroll/screenshot/$',
        reports_views.ScreenShotCreateView.as_view()),

    url(r'^scroll/heat/map/(?P<screenshot_id>[0-9]+)/(?P<pk>[0-9]+)/(?P<path>.*)$',
        reports_views.ScrollHeatMapCanvasView.as_view()),
]

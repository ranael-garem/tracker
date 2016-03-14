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
]

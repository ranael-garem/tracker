from django.conf.urls import include, url
from django.contrib import admin
from tracker.views import IndexView


urlpatterns = [
    url(r'^', include('logger.urls')),

    url(r'^auth/', include('authentication.urls')),

    url(r'^reports/', include('reports.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),

    url('^.*$', IndexView.as_view(), name='index'),

]

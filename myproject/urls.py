from django.conf.urls import include, url
from django.contrib import admin
from myproject.views import IndexView
from myproject import settings

urlpatterns = [
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include('logger.urls')),

    url(r'^auth/', include('authentication.urls')),

    url(r'^reports/', include('reports.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),

    url('^.*$', IndexView.as_view(), name='index'),

]

if settings.DEPLOYED:
    urlpatterns += [url(r'^static/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': settings.STATIC_ROOT}), ]

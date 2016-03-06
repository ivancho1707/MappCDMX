from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^alerts/?$', 'alerts'),
    url(r'^planTrip/?$', 'plan_trip'),
    url(r'^stops/?$', 'stops'),
    url(r'^routes/?$', 'routes'),
    url(r'^routes/(?P<tripId>.*)/geometry/?$', 'geometry'),
)
from django.conf.urls import patterns, url

urlpatterns = patterns('mapp.views',
    url(r'^$', 'map_viewer'),
)
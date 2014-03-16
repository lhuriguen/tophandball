from django.conf.urls import patterns, url

from data import views


urlpatterns = patterns(
    '',
    # ex: /data/
    url(r'^$', views.index, name='index'),
    # ex: /data/clubs/
    url(r'^clubs/$',
        views.IndexView.as_view(), name='club_index'),
    # ex: /data/clubs/1/
    url(r'^clubs/(?P<pk>\d+)/$',
        views.DetailView.as_view(), name='club_detail'),
    # ex: /data/clubs/1/edit/
    url(r'^clubs/(?P<pk>\d+)/edit/$',
        views.ClubUpdateView.as_view(), name='club_update')
    )

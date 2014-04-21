from django.conf.urls import patterns, url

from data import views


urlpatterns = patterns(
    '',
    # ex: /data/
    url(r'^$', views.index, name='index'),
    # ex: /data/clubs/
    url(r'^clubs/$',
        views.ClubIndexView.as_view(), name='club_index'),
    # ex: /data/clubs/1/
    url(r'^clubs/(?P<pk>\d+)/$',
        views.ClubDetailView.as_view(), name='club_detail'),
    # ex: /data/clubs/1/edit/
    url(r'^clubs/(?P<pk>\d+)/edit/$',
        views.ClubUpdateView.as_view(), name='club_update'),
    # ex: /data/clubs/1/matches/
    url(r'^clubs/(?P<pk>\d+)/matches/$',
        views.ClubMatchView.as_view(), name='club_matches'),
    # ex: /data/players/
    url(r'^players/$',
        views.PlayerIndexView.as_view(), name='player_index'),
    # ex: /data/players/1/
    url(r'^players/(?P<pk>\d+)/$',
        views.PlayerDetailView.as_view(), name='player_detail'),
    # ex: /data/players/1/edit/
    # url(r'^players/(?P<pk>\d+)/edit/$',
    #     views.PlayerUpdateView.as_view(), name='player_update')
    # ex: /data/comp/
    url(r'^comp/$',
        views.CompIndexView.as_view(), name='comp_index'),
    # ex: /data/comp/1/
    url(r'^comp/(?P<pk>\d+)/$',
        views.CompDetailView.as_view(), name='comp_detail'),
    # ex: /data/comp/1/edit/
    # url(r'^comp/(?P<pk>\d+)/edit/$',
    #     views.CompUpdateView.as_view(), name='comp_update')
    )

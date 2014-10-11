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
    # ex: /data/clubs/1/team/
    url(r'^clubs/(?P<pk>\d+)/team/$',
        views.ClubTeamView.as_view(), name='club_team'),
    # ex: /data/clubs/1/team/edit/
    url(r'^clubs/(?P<pk>\d+)/team/edit/$',
        views.ClubTeamEditView.as_view(), name='club_team_edit'),
    # ex: /data/clubs/1/love/
    url(r'^clubs/(?P<club_id>\d+)/love/$',
        views.club_love, name='club_love'),
    # ex: /data/clubs/1/club-name-slug/
    url(r'^clubs/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$',
        views.ClubDetailView.as_view(), name='club_detail'),
    # ex: /data/players/
    url(r'^players/$',
        views.PlayerIndexView.as_view(), name='player_index'),
    # ex: /data/players/1/
    url(r'^players/(?P<pk>\d+)/$',
        views.PlayerDetailView.as_view(), name='player_detail'),
    # ex: /data/players/1/edit/
    url(r'^players/(?P<pk>\d+)/edit/$',
        views.PlayerUpdateView.as_view(), name='player_update'),
    # ex: /data/players/1/love/
    url(r'^players/(?P<player_id>\d+)/love/$',
        views.player_love, name='player_love'),
    # ex: /data/players/1/player-name-slug/
    url(r'^players/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$',
        views.PlayerDetailView.as_view(), name='player_detail'),
    # ex: /data/comp/
    url(r'^comp/$',
        views.CompIndexView.as_view(), name='comp_index'),
    # ex: /data/comp/1/
    url(r'^comp/(?P<pk>\d+)/$',
        views.CompDetailView.as_view(), name='comp_detail'),
    # ex: /data/comp/1/edit/
    url(r'^comp/(?P<pk>\d+)/edit/$',
        views.CompUpdateView.as_view(), name='comp_update'),
    # ex: /data/comp/1/comp-name-slug
    url(r'^comp/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$',
        views.CompDetailView.as_view(), name='comp_detail'),
    # API test
    url(r'api/player_search/$',
        views.PlayerJSONView.as_view(), name='player_search_api'),
    url(r'api/player/(?P<pk>\d+)/$',
        views.PlayerAPIView.as_view(), name='player_get_api'),
    # Generic unfollow
    url(r'unfollow/$', views.unfollow, name='unfollow')
    )

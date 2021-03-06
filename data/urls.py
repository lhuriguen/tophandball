from django.conf.urls import patterns, url

from data import views


urlpatterns = patterns(
    '',
    # ex: /data/
    url(r'^$', views.index, name='index'),
    # Club urls:
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
    # Player urls:
    # ex: /data/players/
    url(r'^players/$',
        views.PlayerIndexView.as_view(), name='player_index'),
    # ex: /data/players/1/
    url(r'^players/(?P<pk>\d+)/$',
        views.PlayerDetailView.as_view(), name='player_detail'),
    # ex: /data/players/1/edit/
    url(r'^players/(?P<pk>\d+)/edit/$',
        views.PlayerUpdateView.as_view(), name='player_update'),
    # ex: /data/players/1/matches/
    url(r'^players/(?P<pk>\d+)/matches/$',
        views.PlayerMatchView.as_view(), name='player_matches'),
    # ex: /data/players/1/love/
    url(r'^players/(?P<player_id>\d+)/love/$',
        views.player_love, name='player_love'),
    # ex: /data/players/1/player-name-slug/
    url(r'^players/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$',
        views.PlayerDetailView.as_view(), name='player_detail'),
    # Competition urls:
    # ex: /data/comp/
    url(r'^comp/$',
        views.CompIndexView.as_view(), name='comp_index'),
    # ex: /data/comp/1/
    url(r'^comp/(?P<pk>\d+)/$',
        views.CompDetailView.as_view(), name='comp_detail'),
    # ex: /data/comp/1/edit/
    # url(r'^comp/(?P<pk>\d+)/edit/$',
    #     views.CompUpdateView.as_view(), name='comp_update'),
    # ex: /data/comp/1/season_year/
    url(r'^comp/(?P<comp_id>\d+)/(?P<year>\d\d\d\d)/$',
        views.CompSeasonRedirectView.as_view(), name='comp_season'),
    # ex: /data/comp/1/season_year/stats/
    url(r'^comp/(?P<comp_id>\d+)/(?P<year>\d\d\d\d)/stats/$',
        views.CompSeasonStatsView.as_view(), name='comp_season_stats'),
    # ex: /data/comp/1/season_year/teams/
    url(r'^comp/(?P<comp_id>\d+)/(?P<year>\d\d\d\d)/teams/$',
        views.CompSeasonTeamsView.as_view(), name='comp_season_teams'),
    # ex: /data/comp/1/season_year/7/
    url(r'^comp/(?P<comp_id>\d+)/(?P<year>\d\d\d\d)/(?P<pk>\d+)/$',
        views.StageDetailView.as_view(), name='stage_detail'),
    # ex: /data/comp/1/comp-name-slug
    url(r'^comp/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$',
        views.CompDetailView.as_view(), name='comp_detail'),
    # ex: /data/matches/1/
    url(r'^matches/(?P<pk>\d+)/$',
        views.MatchDetailView.as_view(), name='match_detail'),
    # API test
    url(r'api/club_search/$',
        views.ClubJSONView.as_view(), name='club_search_api'),
    url(r'api/club/(?P<pk>\d+)/$',
        views.ClubAPIView.as_view(), name='club_get_api'),
    url(r'api/player_search/$',
        views.PlayerJSONView.as_view(), name='player_search_api'),
    url(r'api/player/(?P<pk>\d+)/$',
        views.PlayerAPIView.as_view(), name='player_get_api'),
    url(r'api/search_all/$',
        views.SearchJSONView.as_view(), name='search_all_api'),
    # ex: /data/comp/1/season_year/map/
    url(r'^comp/(?P<comp_id>\d+)/(?P<year>\d\d\d\d)/map/$',
        views.CompSeasonMapView.as_view(), name='comp_season_map'),
    # Generic unfollow
    url(r'unfollow/$', views.unfollow, name='unfollow')
    )

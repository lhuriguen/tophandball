# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Club'
        db.create_table(u'data_club', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('ehf_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('twitter', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'data', ['Club'])

        # Adding model 'Season'
        db.create_table(u'data_season', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('year_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'data', ['Season'])

        # Adding unique constraint on 'Season', fields ['year_from', 'year_to']
        db.create_unique(u'data_season', ['year_from', 'year_to'])

        # Adding model 'ClubName'
        db.create_table(u'data_clubname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Club'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Season'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'data', ['ClubName'])

        # Adding model 'Player'
        db.create_table(u'data_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('ehf_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('position', self.gf('django.db.models.fields.CharField')(default='U', max_length=2)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('main_hand', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('retired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'data', ['Player'])

        # Adding model 'PlayerName'
        db.create_table(u'data_playername', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Player'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'data', ['PlayerName'])

        # Adding model 'PlayerContract'
        db.create_table(u'data_playercontract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Player'])),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Club'])),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('shirt_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'data', ['PlayerContract'])

        # Adding model 'Coach'
        db.create_table(u'data_coach', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Player'], unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'data', ['Coach'])

        # Adding model 'CoachContract'
        db.create_table(u'data_coachcontract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coach', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Coach'])),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Club'])),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'data', ['CoachContract'])

        # Adding model 'Competition'
        db.create_table(u'data_competition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('is_international', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'data', ['Competition'])

        # Adding model 'CompetitionSeason'
        db.create_table(u'data_competitionseason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Competition'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Season'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'data', ['CompetitionSeason'])

        # Adding unique constraint on 'CompetitionSeason', fields ['competition', 'season']
        db.create_unique(u'data_competitionseason', ['competition_id', 'season_id'])

        # Adding model 'Stage'
        db.create_table(u'data_stage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comp_season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.CompetitionSeason'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'data', ['Stage'])

        # Adding model 'Group'
        db.create_table(u'data_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Stage'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('is_single', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'data', ['Group'])

        # Adding M2M table for field teams on 'Group'
        m2m_table_name = db.shorten_name(u'data_group_teams')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'data.group'], null=False)),
            ('club', models.ForeignKey(orm[u'data.club'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'club_id'])

        # Adding model 'Match'
        db.create_table(u'data_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Stage'])),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_matches', to=orm['data.Club'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_matches', to=orm['data.Club'])),
            ('placeholder', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('arena', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('spectators', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('score_home', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('score_away', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('report_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'data', ['Match'])

        # Adding M2M table for field referees on 'Match'
        m2m_table_name = db.shorten_name(u'data_match_referees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'data.match'], null=False)),
            ('referee', models.ForeignKey(orm[u'data.referee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['match_id', 'referee_id'])

        # Adding M2M table for field delegates on 'Match'
        m2m_table_name = db.shorten_name(u'data_match_delegates')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'data.match'], null=False)),
            ('delegate', models.ForeignKey(orm[u'data.delegate'], null=False))
        ))
        db.create_unique(m2m_table_name, ['match_id', 'delegate_id'])

        # Adding model 'MatchTeamStats'
        db.create_table(u'data_matchteamstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Match'])),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Club'])),
            ('halftime_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('finaltime_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('score_et1', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('score_et2', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('score_7m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('given_7m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('goals_7m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('timeout1', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('timeout2', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('timeout3', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('yellow_card', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('two_minutes', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('red_card', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'data', ['MatchTeamStats'])

        # Adding unique constraint on 'MatchTeamStats', fields ['match', 'club']
        db.create_unique(u'data_matchteamstats', ['match_id', 'club_id'])

        # Adding model 'MatchPlayerStats'
        db.create_table(u'data_matchplayerstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.MatchTeamStats'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Player'])),
            ('goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('goals_7m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('goals_shots', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('saves', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('saves_7m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('saves_shots', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('yellow_card', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('two_minutes', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('red_card', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'data', ['MatchPlayerStats'])

        # Adding unique constraint on 'MatchPlayerStats', fields ['match_team', 'player']
        db.create_unique(u'data_matchplayerstats', ['match_team_id', 'player_id'])

        # Adding model 'Referee'
        db.create_table(u'data_referee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('pair', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Referee'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'data', ['Referee'])

        # Adding model 'Delegate'
        db.create_table(u'data_delegate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'data', ['Delegate'])


    def backwards(self, orm):
        # Removing unique constraint on 'MatchPlayerStats', fields ['match_team', 'player']
        db.delete_unique(u'data_matchplayerstats', ['match_team_id', 'player_id'])

        # Removing unique constraint on 'MatchTeamStats', fields ['match', 'club']
        db.delete_unique(u'data_matchteamstats', ['match_id', 'club_id'])

        # Removing unique constraint on 'CompetitionSeason', fields ['competition', 'season']
        db.delete_unique(u'data_competitionseason', ['competition_id', 'season_id'])

        # Removing unique constraint on 'Season', fields ['year_from', 'year_to']
        db.delete_unique(u'data_season', ['year_from', 'year_to'])

        # Deleting model 'Club'
        db.delete_table(u'data_club')

        # Deleting model 'Season'
        db.delete_table(u'data_season')

        # Deleting model 'ClubName'
        db.delete_table(u'data_clubname')

        # Deleting model 'Player'
        db.delete_table(u'data_player')

        # Deleting model 'PlayerName'
        db.delete_table(u'data_playername')

        # Deleting model 'PlayerContract'
        db.delete_table(u'data_playercontract')

        # Deleting model 'Coach'
        db.delete_table(u'data_coach')

        # Deleting model 'CoachContract'
        db.delete_table(u'data_coachcontract')

        # Deleting model 'Competition'
        db.delete_table(u'data_competition')

        # Deleting model 'CompetitionSeason'
        db.delete_table(u'data_competitionseason')

        # Deleting model 'Stage'
        db.delete_table(u'data_stage')

        # Deleting model 'Group'
        db.delete_table(u'data_group')

        # Removing M2M table for field teams on 'Group'
        db.delete_table(db.shorten_name(u'data_group_teams'))

        # Deleting model 'Match'
        db.delete_table(u'data_match')

        # Removing M2M table for field referees on 'Match'
        db.delete_table(db.shorten_name(u'data_match_referees'))

        # Removing M2M table for field delegates on 'Match'
        db.delete_table(db.shorten_name(u'data_match_delegates'))

        # Deleting model 'MatchTeamStats'
        db.delete_table(u'data_matchteamstats')

        # Deleting model 'MatchPlayerStats'
        db.delete_table(u'data_matchplayerstats')

        # Deleting model 'Referee'
        db.delete_table(u'data_referee')

        # Deleting model 'Delegate'
        db.delete_table(u'data_delegate')


    models = {
        u'data.club': {
            'Meta': {'object_name': 'Club'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'coaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Coach']", 'through': u"orm['data.CoachContract']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'ehf_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Player']", 'through': u"orm['data.PlayerContract']", 'symmetrical': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'data.clubname': {
            'Meta': {'object_name': 'ClubName'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Club']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Season']"})
        },
        u'data.coach': {
            'Meta': {'object_name': 'Coach'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'data.coachcontract': {
            'Meta': {'object_name': 'CoachContract'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Club']"}),
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Coach']"}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'data.competition': {
            'Meta': {'object_name': 'Competition'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'seasons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Season']", 'through': u"orm['data.CompetitionSeason']", 'symmetrical': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'data.competitionseason': {
            'Meta': {'unique_together': "(('competition', 'season'),)", 'object_name': 'CompetitionSeason'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Competition']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Season']"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'data.delegate': {
            'Meta': {'object_name': 'Delegate'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_single': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Stage']"}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Club']", 'symmetrical': 'False'})
        },
        u'data.match': {
            'Meta': {'object_name': 'Match'},
            'arena': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': u"orm['data.Club']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'delegates': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Delegate']", 'symmetrical': 'False'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matches'", 'to': u"orm['data.Club']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'referees': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Referee']", 'symmetrical': 'False'}),
            'report_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'score_away': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score_home': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spectators': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Stage']"}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'data.matchplayerstats': {
            'Meta': {'unique_together': "(('match_team', 'player'),)", 'object_name': 'MatchPlayerStats'},
            'goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'goals_7m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'goals_shots': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.MatchTeamStats']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']"}),
            'red_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saves': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'saves_7m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'saves_shots': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'two_minutes': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yellow_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'data.matchteamstats': {
            'Meta': {'unique_together': "(('match', 'club'),)", 'object_name': 'MatchTeamStats'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Club']"}),
            'finaltime_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'given_7m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'goals_7m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'halftime_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Match']"}),
            'red_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score_7m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score_et1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score_et2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timeout1': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'timeout2': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'timeout3': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'two_minutes': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yellow_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'data.player': {
            'Meta': {'object_name': 'Player'},
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'ehf_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'main_hand': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '2'}),
            'retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'data.playercontract': {
            'Meta': {'object_name': 'PlayerContract'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Club']"}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']"}),
            'shirt_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'data.playername': {
            'Meta': {'object_name': 'PlayerName'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']"})
        },
        u'data.referee': {
            'Meta': {'object_name': 'Referee'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pair': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Referee']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'data.season': {
            'Meta': {'unique_together': "(('year_from', 'year_to'),)", 'object_name': 'Season'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'year_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'data.stage': {
            'Meta': {'object_name': 'Stage'},
            'comp_season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.CompetitionSeason']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['data']
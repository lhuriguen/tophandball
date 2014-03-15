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
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=3)),
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
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
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
            ('to_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('shirt_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
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
            ('to_date', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal(u'data', ['CoachContract'])

        # Adding model 'Competition'
        db.create_table(u'data_competition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'data', ['Competition'])

        # Adding model 'CompetitionSeason'
        db.create_table(u'data_competitionseason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Competition'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Season'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('has_playoff', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'data', ['CompetitionSeason'])

        # Adding unique constraint on 'CompetitionSeason', fields ['competition', 'season']
        db.create_unique(u'data_competitionseason', ['competition_id', 'season_id'])

        # Adding model 'Round'
        db.create_table(u'data_round', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'data', ['Round'])

        # Adding model 'Match'
        db.create_table(u'data_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_matches', to=orm['data.Club'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_matches', to=orm['data.Club'])),
            ('date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('time', self.gf('django.db.models.fields.TimeField')(blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'data', ['Match'])


    def backwards(self, orm):
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

        # Deleting model 'Round'
        db.delete_table(u'data_round')

        # Deleting model 'Match'
        db.delete_table(u'data_match')


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
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
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
            'to_date': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        u'data.competition': {
            'Meta': {'object_name': 'Competition'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'data.competitionseason': {
            'Meta': {'unique_together': "(('competition', 'season'),)", 'object_name': 'CompetitionSeason'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Competition']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'has_playoff': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Season']"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'data.match': {
            'Meta': {'object_name': 'Match'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': u"orm['data.Club']"}),
            'date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matches'", 'to': u"orm['data.Club']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.TimeField', [], {'blank': 'True'})
        },
        u'data.player': {
            'Meta': {'object_name': 'Player'},
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'ehf_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
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
            'shirt_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        u'data.playername': {
            'Meta': {'object_name': 'PlayerName'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']"})
        },
        u'data.round': {
            'Meta': {'object_name': 'Round'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'data.season': {
            'Meta': {'unique_together': "(('year_from', 'year_to'),)", 'object_name': 'Season'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'year_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['data']
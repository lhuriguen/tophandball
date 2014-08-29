# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'data_country')


        # Changing field 'Competition.country'
        db.alter_column(u'data_competition', 'country', self.gf('django_countries.fields.CountryField')(default='', max_length=2))
        # Adding field 'Delegate.country_iso'
        db.add_column(u'data_delegate', 'country_iso',
                      self.gf('django_countries.fields.CountryField')(default='', max_length=2),
                      keep_default=False)

        # Adding field 'Referee.country_iso'
        db.add_column(u'data_referee', 'country_iso',
                      self.gf('django_countries.fields.CountryField')(default='', max_length=2),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'data_country', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'data', ['Country'])


        # Changing field 'Competition.country'
        db.alter_column(u'data_competition', 'country', self.gf('django.db.models.fields.CharField')(max_length=3, null=True))
        # Deleting field 'Delegate.country_iso'
        db.delete_column(u'data_delegate', 'country_iso')

        # Deleting field 'Referee.country_iso'
        db.delete_column(u'data_referee', 'country_iso')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.club': {
            'Meta': {'object_name': 'Club'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'coaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Coach']", 'symmetrical': 'False', 'through': u"orm['data.CoachContract']", 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'ehf_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fans': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fav_clubs'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Player']", 'symmetrical': 'False', 'through': u"orm['data.PlayerContract']", 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
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
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'data.coachcontract': {
            'Meta': {'object_name': 'CoachContract'},
            'arrival_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Club']"}),
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Coach']"}),
            'departure_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Season']"})
        },
        u'data.competition': {
            'Meta': {'object_name': 'Competition'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'country_iso': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.group': {
            'Meta': {'ordering': "['order']", 'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_single': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Stage']"}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Club']", 'through': u"orm['data.GroupTable']", 'symmetrical': 'False'})
        },
        u'data.grouptable': {
            'Meta': {'ordering': "['position']", 'unique_together': "(('group', 'team'),)", 'object_name': 'GroupTable'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point_penalty': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Club']"})
        },
        u'data.match': {
            'Meta': {'object_name': 'Match'},
            'arena': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': u"orm['data.Club']"}),
            'delegates': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Delegate']", 'symmetrical': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Group']"}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matches'", 'to': u"orm['data.Club']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'match_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'placeholder': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'referees': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Referee']", 'symmetrical': 'False'}),
            'report_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'score_away': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score_home': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spectators': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'week': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
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
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'ehf_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'fans': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fav_players'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'main_hand': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '2'}),
            'retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'retirement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'data.playercontract': {
            'Meta': {'object_name': 'PlayerContract'},
            'arrival_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Club']"}),
            'departure_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Season']"}),
            'shirt_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'})
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
            'country_iso': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pair': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Referee']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'data.season': {
            'Meta': {'unique_together': "(('year_from', 'year_to'),)", 'object_name': 'Season'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'year_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'data.stage': {
            'Meta': {'ordering': "['order']", 'object_name': 'Stage'},
            'comp_season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.CompetitionSeason']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_qualification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['data']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Coach.role'
        db.delete_column(u'data_coach', 'role')

        # Adding field 'CoachContract.role'
        db.add_column(u'data_coachcontract', 'role',
                      self.gf('django.db.models.fields.CharField')(default='H', max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Coach.role'
        db.add_column(u'data_coach', 'role',
                      self.gf('django.db.models.fields.CharField')(default='H', max_length=1),
                      keep_default=False)

        # Deleting field 'CoachContract.role'
        db.delete_column(u'data_coachcontract', 'role')


    models = {
        u'data.club': {
            'Meta': {'object_name': 'Club'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'coaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Coach']", 'through': u"orm['data.CoachContract']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'ehf_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data.Player']", 'through': u"orm['data.PlayerContract']", 'symmetrical': 'False'}),
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
            'role': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
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
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'main_hand': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '2'}),
            'retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'retirement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
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
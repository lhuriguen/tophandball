# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CoachContract.to_date'
        db.alter_column(u'data_coachcontract', 'to_date', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # Changing field 'CoachContract.to_date'
        db.alter_column(u'data_coachcontract', 'to_date', self.gf('django.db.models.fields.DateField')(default=''))

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
            'to_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
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
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'refereeA': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'refereeB': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
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
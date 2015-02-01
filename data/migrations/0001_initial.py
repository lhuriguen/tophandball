# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import data.models
import django_countries.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('display_order', models.SmallIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(help_text=b'For use as common name, ex. Vardar, Hypo, FCM...', max_length=15, blank=True)),
                ('initials', models.CharField(help_text=b'For use in matches, ex. GYO, VAR, BUD...', max_length=3, blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('ehf_id', models.IntegerField(unique=True, verbose_name=b'EHF id')),
                ('address', models.CharField(help_text=b'Separate address items with commas.', max_length=200, blank=True)),
                ('website', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'clubs', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClubName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('club', models.ForeignKey(to='data.Club')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('birth_place', models.CharField(max_length=50, null=True, blank=True)),
                ('gender', models.CharField(default=b'F', max_length=1, choices=[(b'F', b'Female'), (b'M', b'Male')])),
                ('photo', models.ImageField(null=True, upload_to=b'people', blank=True)),
            ],
            options={
                'verbose_name_plural': 'coaches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoachContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departure_month', models.IntegerField(blank=True, help_text=b'Only if the person left before the end of the season.', null=True, choices=[(1, b'January'), (2, b'February'), (3, b'March'), (4, b'April'), (5, b'May'), (6, b'June'), (7, b'July'), (8, b'August'), (9, b'September'), (10, b'October'), (11, b'November'), (12, b'December')])),
                ('arrival_month', models.IntegerField(blank=True, help_text=b'Only if the person arrived after the start of the season.', null=True, choices=[(1, b'January'), (2, b'February'), (3, b'March'), (4, b'April'), (5, b'May'), (6, b'June'), (7, b'July'), (8, b'August'), (9, b'September'), (10, b'October'), (11, b'November'), (12, b'December')])),
                ('role', models.CharField(default=b'H', max_length=1, choices=[(b'H', b'Head coach'), (b'A', b'Assistant coach')])),
                ('club', models.ForeignKey(to='data.Club')),
                ('coach', models.ForeignKey(to='data.Coach')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=5)),
                ('website', models.URLField(blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('is_international', models.BooleanField(default=False)),
                ('level', models.PositiveSmallIntegerField(default=1)),
                ('logo', models.ImageField(null=True, upload_to=b'comps', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompetitionSeason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('competition', models.ForeignKey(to='data.Competition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Delegate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField(verbose_name=b'Group order')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('start_points', models.SmallIntegerField(default=0, help_text=b'Additional points to add or take away.')),
                ('group', models.ForeignKey(to='data.Group')),
                ('team', models.ForeignKey(to='data.Club')),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match_datetime', models.DateTimeField()),
                ('arena', models.CharField(max_length=100, blank=True)),
                ('location', models.CharField(max_length=100, blank=True)),
                ('spectators', models.PositiveIntegerField(null=True, blank=True)),
                ('score_home', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('score_away', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('report_url', models.URLField(blank=True)),
                ('week', models.SmallIntegerField(default=0)),
                ('away_team', models.ForeignKey(related_name='away_matches', to='data.Club')),
                ('delegates', models.ManyToManyField(to='data.Delegate', blank=True)),
                ('group', models.ForeignKey(to='data.Group')),
                ('home_team', models.ForeignKey(related_name='home_matches', to='data.Club')),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchPlayerStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('goals_7m', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('goals_shots', models.PositiveSmallIntegerField(null=True, verbose_name=b'Shots made', blank=True)),
                ('saves', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('saves_7m', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('saves_shots', models.PositiveSmallIntegerField(null=True, verbose_name=b'Shots received', blank=True)),
                ('yellow_card', models.BooleanField(default=False)),
                ('two_minutes', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('red_card', models.BooleanField(default=False)),
                ('club', models.ForeignKey(to='data.Club')),
                ('match', models.ForeignKey(to='data.Match')),
            ],
            options={
                'verbose_name_plural': 'player stats',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchTeamStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('halftime_score', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('finaltime_score', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('score_pt', models.PositiveSmallIntegerField(null=True, verbose_name=b'Score after playing time', blank=True)),
                ('score_et1', models.PositiveSmallIntegerField(null=True, verbose_name=b'Score after ET1', blank=True)),
                ('score_et2', models.PositiveSmallIntegerField(null=True, verbose_name=b'Score after ET2', blank=True)),
                ('score_7m', models.PositiveSmallIntegerField(null=True, verbose_name=b'Score after 7m shootout', blank=True)),
                ('given_7m', models.PositiveSmallIntegerField(null=True, verbose_name=b'7m given', blank=True)),
                ('goals_7m', models.PositiveSmallIntegerField(null=True, verbose_name=b'7m scored', blank=True)),
                ('timeout1', models.CharField(max_length=10, blank=True)),
                ('timeout2', models.CharField(max_length=10, blank=True)),
                ('timeout3', models.CharField(max_length=10, blank=True)),
                ('yellow_card', models.BooleanField(default=False)),
                ('two_minutes', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('red_card', models.BooleanField(default=False)),
                ('club', models.ForeignKey(to='data.Club')),
                ('match', models.ForeignKey(to='data.Match')),
            ],
            options={
                'verbose_name_plural': 'team stats',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('birth_place', models.CharField(max_length=50, null=True, blank=True)),
                ('gender', models.CharField(default=b'F', max_length=1, choices=[(b'F', b'Female'), (b'M', b'Male')])),
                ('photo', models.ImageField(null=True, upload_to=b'people', blank=True)),
                ('ehf_id', models.IntegerField(unique=True, verbose_name=b'EHF id')),
                ('position', models.CharField(default=b'U', max_length=2, choices=[(b'GK', b'Goalkeeper'), (b'LP', b'Line player'), (b'LW', b'Left wing'), (b'RW', b'Right wing'), (b'LB', b'Left back'), (b'RB', b'Right back'), (b'MB', b'Middle back'), (b'B', b'Back'), (b'W', b'Wing'), (b'U', b'Unknown')])),
                ('height', models.PositiveSmallIntegerField(default=0, help_text=b'Please indicate height in centimeters.', blank=True)),
                ('main_hand', models.CharField(default=b'U', max_length=1, choices=[(b'L', b'Left'), (b'R', b'Right'), (b'U', b'Unknown')])),
                ('retired', models.BooleanField(default=False)),
                ('retirement_date', models.DateField(null=True, blank=True)),
                ('fans', models.ManyToManyField(related_name='fav_players', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departure_month', models.IntegerField(blank=True, help_text=b'Only if the person left before the end of the season.', null=True, choices=[(1, b'January'), (2, b'February'), (3, b'March'), (4, b'April'), (5, b'May'), (6, b'June'), (7, b'July'), (8, b'August'), (9, b'September'), (10, b'October'), (11, b'November'), (12, b'December')])),
                ('arrival_month', models.IntegerField(blank=True, help_text=b'Only if the person arrived after the start of the season.', null=True, choices=[(1, b'January'), (2, b'February'), (3, b'March'), (4, b'April'), (5, b'May'), (6, b'June'), (7, b'July'), (8, b'August'), (9, b'September'), (10, b'October'), (11, b'November'), (12, b'December')])),
                ('shirt_number', models.PositiveSmallIntegerField(default=0, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=data.models.player_contract_filename, blank=True)),
                ('club', models.ForeignKey(to='data.Club')),
                ('player', models.ForeignKey(to='data.Player')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('player', models.ForeignKey(to='data.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Referee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='data.Referee', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year_from', models.PositiveSmallIntegerField(db_index=True)),
                ('year_to', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField(verbose_name=b'Stage order')),
                ('name', models.CharField(max_length=30)),
                ('short_name', models.CharField(max_length=5)),
                ('is_qualification', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=2, choices=[(b'KO', b'Knockout'), (b'RR', b'Round robin'), (b'KG', b'Knockout groups')])),
                ('comp_season', models.ForeignKey(verbose_name=b'Competition Season', to='data.CompetitionSeason')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together=set([('year_from', 'year_to')]),
        ),
        migrations.AddField(
            model_name='playercontract',
            name='season',
            field=models.ForeignKey(to='data.Season'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='matchteamstats',
            unique_together=set([('match', 'club')]),
        ),
        migrations.AddField(
            model_name='matchplayerstats',
            name='player',
            field=models.ForeignKey(to='data.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='matchplayerstats',
            unique_together=set([('match', 'club', 'player')]),
        ),
        migrations.AddField(
            model_name='match',
            name='referees',
            field=models.ManyToManyField(to='data.Referee', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='grouptable',
            unique_together=set([('group', 'team')]),
        ),
        migrations.AddField(
            model_name='group',
            name='stage',
            field=models.ForeignKey(to='data.Stage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='teams',
            field=models.ManyToManyField(to='data.Club', through='data.GroupTable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competitionseason',
            name='season',
            field=models.ForeignKey(to='data.Season'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='competitionseason',
            unique_together=set([('competition', 'season')]),
        ),
        migrations.AddField(
            model_name='competition',
            name='seasons',
            field=models.ManyToManyField(to='data.Season', through='data.CompetitionSeason'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coachcontract',
            name='season',
            field=models.ForeignKey(to='data.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='data.Player', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubname',
            name='season',
            field=models.ForeignKey(to='data.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='coaches',
            field=models.ManyToManyField(to='data.Coach', through='data.CoachContract', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='fans',
            field=models.ManyToManyField(related_name='fav_clubs', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='players',
            field=models.ManyToManyField(to='data.Player', through='data.PlayerContract', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='competitions',
            field=models.ManyToManyField(to='data.Competition', blank=True),
            preserve_default=True,
        ),
    ]

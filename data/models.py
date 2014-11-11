from __future__ import division
import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Q, Sum
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

from django_countries.fields import CountryField


class Season(models.Model):
    year_from = models.PositiveSmallIntegerField(db_index=True)
    year_to = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('year_from', 'year_to')

    @property
    def name(self):
        return '%s/%s' % (self.year_from, str(self.year_to)[-2:])

    def __unicode__(self):
        return u'%s' % (self.name)

    @staticmethod
    def curr_year():
        today = datetime.datetime.today()
        middle = datetime.datetime(today.year, 7, 1)
        if today < middle:
            return today.year - 1
        return today.year


class Club(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(
        max_length=15, blank=True,
        help_text="For use as common name, ex. Vardar, Hypo, FCM...")
    initials = models.CharField(
        max_length=3, blank=True,
        help_text="For use in matches, ex. GYO, VAR, BUD...")
    country = CountryField()
    ehf_id = models.IntegerField('EHF id', unique=True)
    address = models.CharField(
        max_length=200, blank=True,
        help_text="Separate address items with commas.")
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    logo = models.ImageField(upload_to='clubs', blank=True, null=True)
    players = models.ManyToManyField(
        'Player', through='PlayerContract', blank=True)
    coaches = models.ManyToManyField(
        'Coach', through='CoachContract', blank=True)
    fans = models.ManyToManyField(User, related_name='fav_clubs')

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('data:club_detail',
                       kwargs={'pk': self.pk, 'slug': slugify(self.name)})

    def get_current_team(self):
        today = datetime.datetime.today()
        middle = datetime.datetime(today.year, 7, 1)
        season_year = today.year
        if today < middle:
            season_year -= 1
        return self.playercontract_set.select_related(
            'player', 'season').filter(
            season__year_from=season_year, departure_month=None)

    def get_current_coaches(self):
        today = datetime.datetime.today()
        middle = datetime.datetime(today.year, 7, 1)
        season_year = today.year
        if today < middle:
            season_year -= 1
        return self.coachcontract_set.filter(
            season__year_from=season_year, departure_month=None)

    def get_matches(self):
        query = Q(home_team=self) | Q(away_team=self)
        return Match.objects.filter(query).select_related(
            ).order_by('-match_datetime')

    def address_lines(self):
        if self.address:
            return self.address.split(',')
        return []

    def has_logo(self):
        if self.logo:
            return True
        return False
    has_logo.boolean = True
    has_logo.short_description = 'Has logo?'

    def admin_thumbnail(self):
        if self.logo:
            return u'<img src="%s" />' % (self.logo.url)
        else:
            return u'No image.'
    admin_thumbnail.short_description = 'Logo preview'
    admin_thumbnail.allow_tags = True

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        else:
            return u'http://placehold.it/200x200&text=No+Logo'

    @property
    def display_name(self):
        return self.short_name or self.name


class ClubName(models.Model):
    club = models.ForeignKey(Club)
    season = models.ForeignKey(Season)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.season)


class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((FEMALE, 'Female'), (MALE, 'Male'))

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = CountryField()
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=FEMALE)
    photo = models.ImageField(upload_to='people', blank=True, null=True)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def age(self):
        today = datetime.date.today()
        born = self.birth_date
        adjust = ((today.month, today.day) < (born.month, born.day))
        return today.year - born.year - adjust

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return u'http://placehold.it/320x400&text=No+Image'

    class Meta:
        abstract = True

    def has_photo(self):
        if self.photo:
            return True
        return False
    has_photo.boolean = True
    has_photo.short_description = 'Has photo?'

    def admin_thumbnail(self):
        if self.photo:
            return u'<img style="height: 300px;" src="%s" />' % (
                self.photo.url)
        else:
            return u'No image.'
    admin_thumbnail.short_description = 'Photo preview'
    admin_thumbnail.allow_tags = True


class Player(Person):
    UNKNOWN = 'U'
    GOALKEEPER = 'GK'
    LINE_PLAYER = 'LP'
    LEFT_WING = 'LW'
    RIGHT_WING = 'RW'
    LEFT_BACK = 'LB'
    RIGHT_BACK = 'RB'
    MIDDLE_BACK = 'MB'
    BACK = 'B'
    WING = 'W'
    POSITION_CHOICES = (
        (GOALKEEPER, 'Goalkeeper'),
        (LINE_PLAYER, 'Line player'),
        (LEFT_WING, 'Left wing'),
        (RIGHT_WING, 'Right wing'),
        (LEFT_BACK, 'Left back'),
        (RIGHT_BACK, 'Right back'),
        (MIDDLE_BACK, 'Middle back'),
        (BACK, 'Back'),
        (WING, 'Wing'),
        (UNKNOWN, 'Unknown')
    )

    LEFT_HAND = 'L'
    RIGHT_HAND = 'R'
    HAND_CHOICES = (
        (LEFT_HAND, 'Left'),
        (RIGHT_HAND, 'Right'),
        (UNKNOWN, 'Unknown')
    )

    ehf_id = models.IntegerField('EHF id', unique=True)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=UNKNOWN)
    height = models.PositiveSmallIntegerField(
        blank=True, default=0,
        help_text="Please indicate height in centimeters.")
    main_hand = models.CharField(
        max_length=1, choices=HAND_CHOICES, default=UNKNOWN)
    retired = models.BooleanField(default=False)
    retirement_date = models.DateField(null=True, blank=True)
    fans = models.ManyToManyField(User, related_name='fav_players')

    def __unicode__(self):
        return u'%s' % (self.full_name)

    @property
    def is_goalkeeper(self):
        return self.position == Player.GOALKEEPER

    def get_absolute_url(self):
        return reverse('data:player_detail',
                       kwargs={'pk': self.pk, 'slug': slugify(self.full_name)})

    @property
    def current_contract(self):
        today = datetime.datetime.today()
        middle = datetime.datetime(today.year, 7, 1)
        season_year = today.year
        if today < middle:
            season_year -= 1
        contracts = self.playercontract_set.select_related(
            'club', 'season').filter(
            season__year_from=season_year, departure_month=None)
        if len(contracts) == 1:
            return contracts[0]
        else:
            return None


class PlayerName(models.Model):
    player = models.ForeignKey(Player)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return u'%s - %s %s' % (self.player, self.first_name, self.last_name)


class Contract(models.Model):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12
    MONTH_CHOICES = (
        (JANUARY, 'January'),
        (FEBRUARY, 'February'),
        (MARCH, 'March'),
        (APRIL, 'April'),
        (MAY, 'May'),
        (JUNE, 'June'),
        (JULY, 'July'),
        (AUGUST, 'August'),
        (SEPTEMBER, 'September'),
        (OCTOBER, 'October'),
        (NOVEMBER, 'November'),
        (DECEMBER, 'December')
    )
    club = models.ForeignKey(Club)
    season = models.ForeignKey(Season)
    departure_month = models.IntegerField(
        choices=MONTH_CHOICES, blank=True, null=True,
        help_text="Only if the person left before the end of the season.")
    arrival_month = models.IntegerField(
        choices=MONTH_CHOICES, blank=True, null=True,
        help_text="Only if the person arrived after the start of the season.")

    class Meta:
        abstract = True


class PlayerContract(Contract):

    def player_contract_filename(instance, filename):
        """
        Construct the filepath to store contract photos.
        Ex: /contracts/2013/cid_pid.ext
        """
        ext = filename.split('.')[-1]
        new_file = '%s_%s.%s' % (instance.club_id, instance.player_id, ext)
        return '/'.join([
            'contracts', str(instance.season.year_from), new_file
            ])

    player = models.ForeignKey(Player)
    shirt_number = models.PositiveSmallIntegerField(blank=True, default=0)
    photo = models.ImageField(
        upload_to=player_contract_filename, blank=True, null=True)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return self.player.photo_url

    def __unicode__(self):
        return u'%s (%s) in %s (%s)' % (
            self.player.full_name, self.player.position,
            self.club.name, self.season.name)

    def is_current(self):
        today = datetime.datetime.today()
        middle = datetime.date(today.year, 7, 1)
        season_year = today.year
        if today < middle:
            season_year -= 1
        return self.season.year_from == season_year


class Coach(Person):
    player = models.ForeignKey(Player, blank=True, null=True, unique=True,
                               on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'coaches'

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class CoachContract(Contract):
    HEAD = 'H'
    ASSISTANT = 'A'
    ROLE_CHOICES = (
        (HEAD, 'Head coach'),
        (ASSISTANT, 'Assistant coach')
    )

    coach = models.ForeignKey(Coach)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=HEAD)

    def __unicode__(self):
        return u'%s in %s (%s)' % (
            self.coach.full_name, self.club.name, self.season.name)


class Competition(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    website = models.URLField(blank=True)
    country = CountryField()
    is_international = models.BooleanField(default=False)
    level = models.PositiveSmallIntegerField(default=1)
    logo = models.ImageField(upload_to='comps', blank=True, null=True)
    seasons = models.ManyToManyField(Season, through='CompetitionSeason')

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('data:comp_detail',
                       kwargs={'pk': self.pk, 'slug': slugify(self.name)})

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        else:
            return u'http://placehold.it/200x200&text=No+Logo'

    def has_logo(self):
        if self.logo:
            return True
        return False
    has_logo.boolean = True
    has_logo.short_description = 'Has logo?'

    def admin_thumbnail(self):
        if self.logo:
            return u'<img src="%s" />' % (self.logo.url)
        else:
            return u'No image.'
    admin_thumbnail.short_description = 'Logo preview'
    admin_thumbnail.allow_tags = True

    def get_season_or_latest(self, year=None):
        year = year or datetime.datetime.now().year
        cs = self.competitionseason_set.filter(season__year_to=year)
        if not cs:
            cs = self.competitionseason_set.order_by(
                '-season__year_to')
        if cs:
            return cs[0]
        return None


class CompetitionSeason(models.Model):
    competition = models.ForeignKey(Competition)
    season = models.ForeignKey(Season)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'%s %s' % (self.competition.name, self.season.name)

    def get_absolute_url(self):
        return reverse('data:comp_season',
                       kwargs={'year': self.season.year_from,
                               'comp_id': self.competition.id
                               })

    def get_teams(self):
        return Club.objects.filter(
            grouptable__group__stage__comp_season=self
            ).order_by('name').distinct()

    class Meta:
        unique_together = ('competition', 'season')


class Stage(models.Model):
    """Represents a round or stage in a competition"""

    KNOCKOUT = 'KO'
    ROUND_ROBIN = 'RR'
    KO_GROUPS = 'KG'
    TYPE_CHOICES = (
        (KNOCKOUT, 'Knockout'),
        (ROUND_ROBIN, 'Round robin'),
        (KO_GROUPS, 'Knockout groups')
        )
    comp_season = models.ForeignKey(CompetitionSeason,
                                    verbose_name='Competition Season')
    order = models.PositiveSmallIntegerField('Stage order')
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=5)
    is_qualification = models.BooleanField(default=False)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    def __unicode__(self):
        return u'%s %s. %s' % (self.comp_season, self.order, self.name)

    def get_absolute_url(self):
        return reverse('data:stage_detail',
                       kwargs={'pk': self.pk,
                               'comp_id': self.comp_season.competition.id,
                               'year': self.comp_season.season.year_from
                               })

    def get_teams(self):
        return Club.objects.filter(
            grouptable__group__stage=self
            ).order_by('name')

    class Meta:
        ordering = ['order']


class Group(models.Model):
    stage = models.ForeignKey(Stage)
    order = models.PositiveSmallIntegerField('Group order')
    name = models.CharField(max_length=30)
    teams = models.ManyToManyField(Club, through='GroupTable')

    def __unicode__(self):
        return u'%s - %s' % (self.stage, self.name)

    def get_table(self):
        return GroupTable.objects.filter(
            group=self).select_related('team').order_by('position')

    def get_matches(self):
        return self.match_set.select_related(
            'home_team', 'away_team').order_by('match_datetime')

    class Meta:
        ordering = ['order']


class GroupTable(models.Model):
    group = models.ForeignKey(Group)
    team = models.ForeignKey(Club)
    position = models.PositiveSmallIntegerField(default=0)
    start_points = models.SmallIntegerField(
        default=0, help_text="Additional points to add or take away.")

    def __unicode__(self):
        return u'%s %s' % (self.group, self.team)

    class Meta:
        unique_together = ('group', 'team')
        ordering = ['position']

    def query(self):
        return Q(home_team=self.team) | Q(away_team=self.team)

    @property
    def matches(self):
        return self.group.match_set.filter(self.query()).order_by('date')

    @property
    def num_matches(self):
        return self.group.match_set.filter(self.query()).count()

    @property
    def wins(self):
        home = self.team.home_matches.filter(
            group=self.group, score_home__gt=F('score_away')).count()
        away = self.team.away_matches.filter(
            group=self.group, score_away__gt=F('score_home')).count()
        total = home + away
        return (total, home, away)

    @property
    def draws(self):
        home = self.team.home_matches.filter(
            group=self.group, score_home=F('score_away')).count()
        away = self.team.away_matches.filter(
            group=self.group, score_away=F('score_home')).count()
        total = home + away
        return (total, home, away)

    @property
    def losses(self):
        home = self.team.home_matches.filter(
            group=self.group, score_home__lt=F('score_away')).count()
        away = self.team.away_matches.filter(
            group=self.group, score_away__lt=F('score_home')).count()
        total = home + away
        return (total, home, away)

    @property
    def goals_for(self):
        home = self.team.home_matches.filter(
            group=self.group).aggregate(
            for_home=Sum('score_home'))['for_home']
        away = self.team.away_matches.filter(
            group=self.group).aggregate(
            for_away=Sum('score_away'))['for_away']
        total = int(home or 0) + int(away or 0)
        return (total, home, away)

    @property
    def goals_against(self):
        home = self.team.home_matches.filter(
            group=self.group).aggregate(
            against_home=Sum('score_away'))['against_home']
        away = self.team.away_matches.filter(
            group=self.group).aggregate(
            against_away=Sum('score_home'))['against_away']
        total = int(home or 0) + int(away or 0)
        return (total, home, away)

    @property
    def points(self):
        return self.wins[0] * 2 + self.draws[0] * 1 + self.start_points


class Match(models.Model):
    group = models.ForeignKey(Group)
    home_team = models.ForeignKey(Club, related_name='home_matches')
    away_team = models.ForeignKey(Club, related_name='away_matches')
    match_datetime = models.DateTimeField()
    arena = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    spectators = models.PositiveIntegerField(blank=True, null=True)
    score_home = models.PositiveSmallIntegerField(blank=True, null=True)
    score_away = models.PositiveSmallIntegerField(blank=True, null=True)
    report_url = models.URLField(blank=True)
    week = models.SmallIntegerField(default=0)
    referees = models.ManyToManyField('Referee')
    delegates = models.ManyToManyField('Delegate')

    def __unicode__(self):
        return u'%s vs %s on %s' % (
            self.home_team, self.away_team, self.match_datetime)

    class Meta:
        verbose_name_plural = 'matches'

    def get_absolute_url(self):
        return reverse('data:match_detail', kwargs={'pk': self.pk})

    @property
    def display_result(self):
        if self.score_home and self.score_away:
            return str(self.score_home) + ':' + str(self.score_away)
        return '?:?'

    @property
    def display_halftime(self):
        try:
            home_ht = self.get_home_stats().halftime_score
            away_ht = self.get_away_stats().halftime_score
        except:
            return '?:?'
        return str(home_ht) + ':' + str(away_ht)

    @property
    def is_future(self):
        now = timezone.now()
        return self.match_datetime > now

    @property
    def is_draw(self):
        if self.score_home and self.score_away:
            return self.score_home == self.score_away
        return False

    @property
    def is_home_win(self):
        if self.score_home and self.score_away:
            return self.score_home > self.score_away
        return False

    @property
    def is_away_win(self):
        if self.score_home and self.score_away:
            return self.score_away > self.score_home
        return False

    def get_home_stats(self):
        try:
            return self.matchteamstats_set.get(club=self.home_team)
        except MatchTeamStats.DoesNotExist:
            return None

    def get_home_player_stats(self):
        q = self.matchplayerstats_set.filter(club=self.home_team)
        return q.select_related('player').order_by('-goals')

    def get_away_stats(self):
        try:
            return self.matchteamstats_set.get(club=self.away_team)
        except MatchTeamStats.DoesNotExist:
            return None

    def get_away_player_stats(self):
        q = self.matchplayerstats_set.filter(club=self.away_team)
        return q.select_related('player').order_by('-goals')


class MatchTeamStats(models.Model):
    match = models.ForeignKey(Match)
    club = models.ForeignKey(Club)
    halftime_score = models.PositiveSmallIntegerField(blank=True, null=True)
    finaltime_score = models.PositiveSmallIntegerField(blank=True, null=True)
    score_et1 = models.PositiveSmallIntegerField(
        'Score after ET1', blank=True, null=True)
    score_et2 = models.PositiveSmallIntegerField(
        'Score after ET2', blank=True, null=True)
    score_7m = models.PositiveSmallIntegerField(
        'Score after 7m shootout', blank=True, null=True)
    given_7m = models.PositiveSmallIntegerField(
        '7m given', blank=True, null=True)
    goals_7m = models.PositiveSmallIntegerField(
        '7m scored', blank=True, null=True)
    timeout1 = models.CharField(max_length=10, blank=True)
    timeout2 = models.CharField(max_length=10, blank=True)
    timeout3 = models.CharField(max_length=10, blank=True)
    yellow_card = models.BooleanField(default=False)
    two_minutes = models.PositiveSmallIntegerField(blank=True, null=True)
    red_card = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s in %s' % (self.club, self.match)

    @property
    def first_half_ratio(self):
        return round(self.halftime_score/self.finaltime_score * 100)

    @property
    def second_half_ratio(self):
        return round(self.second_half_score/self.finaltime_score * 100)

    @property
    def second_half_score(self):
        return self.finaltime_score - self.halftime_score

    @property
    def penalty_ratio(self):
        try:
            return round(self.goals_7m/self.given_7m * 100)
        except:
            return 0

    @property
    def penalty_miss_ratio(self):
        try:
            missed = self.given_7m - self.goals_7m
            return round(missed/self.given_7m * 100)
        except:
            return 0

    class Meta:
        verbose_name_plural = 'team stats'
        unique_together = ('match', 'club')


class MatchPlayerStats(models.Model):
    match = models.ForeignKey(Match)
    club = models.ForeignKey(Club)
    player = models.ForeignKey(Player)
    goals = models.PositiveSmallIntegerField(blank=True, null=True)
    goals_7m = models.PositiveSmallIntegerField(blank=True, null=True)
    goals_shots = models.PositiveSmallIntegerField(
        'Shots made', blank=True, null=True)
    saves = models.PositiveSmallIntegerField(blank=True, null=True)
    saves_7m = models.PositiveSmallIntegerField(blank=True, null=True)
    saves_shots = models.PositiveSmallIntegerField(
        'Shots received', blank=True, null=True)
    yellow_card = models.BooleanField(default=False)
    two_minutes = models.PositiveSmallIntegerField(blank=True, null=True)
    red_card = models.BooleanField(default=False)
    # playing_time = models.FloatField(default=0)

    def __unicode__(self):
        return u'%s in %s' % (self.player, self.match)

    class Meta:
        verbose_name_plural = 'player stats'
        unique_together = ('match', 'club', 'player')


class Referee(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()
    pair = models.ForeignKey('self',
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.country)

    def save(self, *args, **kwargs):
        super(Referee, self).save(*args, **kwargs)
        if self.pair:
            self.pair.pair = self


class Delegate(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.country)

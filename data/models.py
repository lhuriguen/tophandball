import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Q, Sum
from django.utils import timezone
from django.contrib.auth.models import User


class Country(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'countries'

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.code)


class Club(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(
        max_length=15, blank=True,
        help_text="For use as common name, ex. Vardar, Hypo, FCM...")
    initials = models.CharField(
        max_length=3, blank=True,
        help_text="For use in matches, ex. GYO, VAR, BUD...")
    country = models.CharField(max_length=3)
    ehf_id = models.IntegerField('EHF id', unique=True)
    address = models.CharField(
        max_length=200, blank=True,
        help_text="Separate address items with commas.")
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    logo = models.ImageField(upload_to='clubs', blank=True, null=True)
    players = models.ManyToManyField('Player', through='PlayerContract')
    coaches = models.ManyToManyField('Coach', through='CoachContract')
    fans = models.ManyToManyField(User, related_name='fav_clubs')

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('data:club_detail', kwargs={'pk': self.pk})

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
        return self.coachcontract_set.exclude(
            to_date__lt=datetime.date.today()
        ).exclude(from_date__gt=datetime.date.today())

    def get_matches(self):
        query = Q(home_team=self) | Q(away_team=self)
        return Match.objects.filter(query).order_by('-match_datetime')

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


class Season(models.Model):
    year_from = models.PositiveSmallIntegerField()
    year_to = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('year_from', 'year_to')

    @property
    def name(self):
        return '%s/%s' % (self.year_from, str(self.year_to)[-2:])

    def __unicode__(self):
        return u'%s' % (self.name)


class ClubName(models.Model):
    club = models.ForeignKey(Club)
    season = models.ForeignKey(Season)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.season)


class Player(models.Model):
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

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((FEMALE, 'Female'), (MALE, 'Male'))

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=3)
    ehf_id = models.IntegerField('EHF id', unique=True)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=UNKNOWN)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=50, blank=True, null=True)
    height = models.PositiveSmallIntegerField(
        blank=True, default=0,
        help_text="Please indicate height in centimeters.")
    main_hand = models.CharField(
        max_length=1, choices=HAND_CHOICES, default=UNKNOWN)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=FEMALE)
    retired = models.BooleanField(default=False)
    retirement_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='people', blank=True, null=True)
    fans = models.ManyToManyField(User, related_name='fav_players')

    def __unicode__(self):
        return u'%s' % (self.full_name)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('data:player_detail', kwargs={'pk': self.pk})

    def has_photo(self):
        if self.photo:
            return True
        return False
    has_photo.boolean = True
    has_photo.short_description = 'Has photo?'

    def admin_thumbnail(self):
        if self.photo:
            return u'<img src="%s" />' % (self.photo.url)
        else:
            return u'No image.'
    admin_thumbnail.short_description = 'Photo preview'
    admin_thumbnail.allow_tags = True

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
            return u'http://placehold.it/160x220&text=No+Image'


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


class PlayerContract(models.Model):
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
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    season = models.ForeignKey(Season)
    departure_month = models.IntegerField(
        choices=MONTH_CHOICES, blank=True, null=True,
        help_text="Only if the player left before the end of the season.")
    arrival_month = models.IntegerField(
        choices=MONTH_CHOICES, blank=True, null=True,
        help_text="Only if the player arrived after the start of the season.")
    shirt_number = models.PositiveSmallIntegerField(blank=True, default=0)

    def __unicode__(self):
        return u'%s (%s) in %s (%s)' % (
            self.player, self.player.position, self.club, self.season)

    def is_current(self):
        today = datetime.datetime.today()
        middle = datetime.date(today.year, 7, 1)
        season_year = today.year
        if today < middle:
            season_year -= 1
        return self.season.year_from == season_year


class Coach(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((FEMALE, 'Female'), (MALE, 'Male'))

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=3)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    player = models.ForeignKey(Player, blank=True, null=True, unique=True,
                               on_delete=models.SET_NULL)
    photo = models.ImageField(upload_to='people', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'coaches'

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return u'http://placehold.it/200x200&text=No+Image'

    def has_photo(self):
        if self.photo:
            return True
        return False
    has_photo.boolean = True
    has_photo.short_description = 'Has photo?'

    def admin_thumbnail(self):
        if self.photo:
            return u'<img src="%s" />' % (self.photo.url)
        else:
            return u'No image.'
    admin_thumbnail.short_description = 'Photo preview'
    admin_thumbnail.allow_tags = True


class CoachContract(models.Model):
    HEAD = 'H'
    ASSISTANT = 'A'
    ROLE_CHOICES = (
        (HEAD, 'Head coach'),
        (ASSISTANT, 'Assistant coach')
    )

    coach = models.ForeignKey(Coach)
    club = models.ForeignKey(Club)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=HEAD)

    def __unicode__(self):
        return u'%s in %s (%s)' % (self.coach, self.club, self.from_date)


class Competition(models.Model):
    # LEAGUE = 'L'
    # CUP = 'C'
    # TYPE_CHOICES = (
    #     (LEAGUE, 'League'),
    #     (CUP, 'Cup')
    #     )
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    #type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    is_international = models.BooleanField(default=False)
    level = models.PositiveSmallIntegerField(default=1)
    logo = models.ImageField(upload_to='comps', blank=True, null=True)
    seasons = models.ManyToManyField(Season, through='CompetitionSeason')

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('data:comp_detail', kwargs={'pk': self.pk})

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
        if not year:
            year = datetime.datetime.now().year
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
    start_date = models.DateField()
    end_date = models.DateField()
    #has_playoff = models.BooleanField()

    def __unicode__(self):
        return u'%s %s' % (self.competition.name, self.season.name)

    class Meta:
        unique_together = ('competition', 'season')


class Stage(models.Model):

    """Represents a round or stage in a competition"""

    comp_season = models.ForeignKey(CompetitionSeason,
                                    verbose_name='Competition Season')
    order = models.PositiveSmallIntegerField('Stage order')
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=5)
    is_qualification = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s. %s' % (self.comp_season, self.order, self.name)

    class Meta:
        ordering = ['order']


class Group(models.Model):
    stage = models.ForeignKey(Stage)
    order = models.PositiveSmallIntegerField('Group order')
    name = models.CharField(max_length=30)
    is_single = models.BooleanField('Is single group?', default=False)
    teams = models.ManyToManyField(Club, through='GroupTable')

    def __unicode__(self):
        return u'%s - %s' % (self.stage, self.name)

    class Meta:
        ordering = ['order']


class GroupTable(models.Model):
    group = models.ForeignKey(Group)
    team = models.ForeignKey(Club)
    position = models.PositiveSmallIntegerField(default=0)
    point_penalty = models.SmallIntegerField(
        default=0, help_text="Points to take away as a penalty.")

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
        return self.wins[0] * 2 + self.draws[0] * 1 - self.point_penalty


class Match(models.Model):
    group = models.ForeignKey(Group)
    home_team = models.ForeignKey(Club, related_name='home_matches')
    away_team = models.ForeignKey(Club, related_name='away_matches')
    placeholder = models.CharField(
        help_text="Placeholder text for use when teams are yet unknown.",
        blank=True, max_length=150)
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

    @property
    def is_future(self):
        now = timezone.now()
        if self.match_datetime > now:
            return True
        return False

    @property
    def is_draw(self):
        if self.score_home and self.score_away:
            return self.score_home == self.score_away
        return False

    @property
    def home_stats(self):
        q = self.matchteamstats_set.filter(club=self.home_team)
        if q.exists():
            return q[0]
        return None

    @property
    def away_stats(self):
        q = self.matchteamstats_set.filter(club=self.away_team)
        if q.exists():
            return q[0]
        return None


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

    class Meta:
        verbose_name_plural = 'team stats'
        unique_together = ('match', 'club')


class MatchPlayerStats(models.Model):
    match_team = models.ForeignKey(MatchTeamStats)
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
    #playing_time = models.FloatField(default=0)

    def __unicode__(self):
        return u'%s in %s' % (self.player, self.match_team)

    class Meta:
        verbose_name_plural = 'player stats'
        unique_together = ('match_team', 'player')


class Referee(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=3)
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
    country = models.CharField(max_length=3)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.country)

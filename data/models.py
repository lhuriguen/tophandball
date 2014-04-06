import datetime

from django.core.urlresolvers import reverse
from django.db import models


class PlayerContractManager(models.Manager):

    @property
    def current(self):
        return super(PlayerContractManager, self).get_queryset().exclude(
            to_date__lt=datetime.date.today()
        ).exclude(from_date__gt=datetime.date.today())


class Club(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3, blank=True)
    country = models.CharField(max_length=3)
    ehf_id = models.IntegerField('EHF id', unique=True)
    address = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    players = models.ManyToManyField('Player', through='PlayerContract')
    coaches = models.ManyToManyField('Coach', through='CoachContract')

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        # return reverse('club_detail', kwargs={'pk': self.pk})
        return reverse('data:club_detail', kwargs={'pk': self.pk})

    def get_current_team(self):
        return self.playercontract_set.exclude(
            to_date__lt=datetime.date.today()
        ).exclude(from_date__gt=datetime.date.today())

    def address_lines(self):
        if self.address:
            return self.address.split(',')
        return []


class Season(models.Model):
    #name = models.CharField(max_length=7)
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
    #clubs = models.ManyToManyField(Club, through='PlayerContract')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    retired = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.full_name)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def is_back_player(self):
        return self.position in (
            self.LEFT_BACK, self.RIGHT_BACK, self.MIDDLE_BACK, self.BACK)

    def get_absolute_url(self):
        return reverse('data:player_detail', kwargs={'pk': self.pk})

    @property
    def current_contract(self):
        contracts = self.playercontract_set.exclude(
            to_date__lt=datetime.date.today()
        ).exclude(from_date__gt=datetime.date.today()).order_by('from_date')
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
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    shirt_number = models.PositiveSmallIntegerField(blank=True, default=0)

    objects = PlayerContractManager()

    def __unicode__(self):
        return u'%s (%s) in %s (%s)' % (
            self.player, self.player.position, self.club, self.from_date)

    def is_current(self):
        today = datetime.date.today()
        if self.to_date is None:
            return self.from_date <= today
        else:
            return self.from_date <= today and self.to_date >= today


class Coach(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((FEMALE, 'Female'), (MALE, 'Male'))

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=3)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    player = models.ForeignKey(Player, blank=True, null=True, unique=True,
                               on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = 'coaches'


class CoachContract(models.Model):
    coach = models.ForeignKey(Coach)
    club = models.ForeignKey(Club)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)

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
    #level = models.PositiveSmallIntegerField(default=1)
    seasons = models.ManyToManyField(Season, through='CompetitionSeason')

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('data:comp_detail', kwargs={'pk': self.pk})


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

    def __unicode__(self):
        return u'%s %s. %s' % (self.comp_season, self.order, self.name)


class Group(models.Model):
    stage = models.ForeignKey(Stage)
    order = models.PositiveSmallIntegerField('Group order')
    name = models.CharField(max_length=30)
    is_single = models.BooleanField('Is single group?', default=False)
    teams = models.ManyToManyField(Club)

    def __unicode__(self):
        return u'%s - %s' % (self.stage, self.name)

# class MatchWeek(models.Model):
#     stage = models.ForeignKey(Stage)
#     order = models.PositiveSmallIntegerField('Match week order')
#     start_date = models.DateField()
#     end_date = models.DateField()


class Match(models.Model):
    stage = models.ForeignKey(Stage)
    home_team = models.ForeignKey(Club, related_name='home_matches')
    away_team = models.ForeignKey(Club, related_name='away_matches')
    placeholder = models.CharField(
        help_text="Placeholder text for use when teams are yet unknown.",
        blank=True, max_length=150)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    arena = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    spectators = models.PositiveIntegerField(blank=True, null=True)
    score_home = models.PositiveSmallIntegerField(blank=True, null=True)
    score_away = models.PositiveSmallIntegerField(blank=True, null=True)
    report_url = models.URLField(blank=True)
    referees = models.ManyToManyField('Referee')
    delegates = models.ManyToManyField('Delegate')

    def __unicode__(self):
        return u'%s vs %s on %s' % (self.home_team, self.away_team, self.date)

    class Meta:
        verbose_name_plural = 'matches'


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

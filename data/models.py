from django.core.urlresolvers import reverse
from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3)
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
        #return reverse('club_detail', kwargs={'pk': self.pk})
        return reverse('data:club_detail', kwargs={'pk': self.pk})


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
        return u'%s - %s (%s)' % (self.club, self.name, self.season)


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


class PlayerName(models.Model):
    player = models.ForeignKey(Player)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s - %s %s' % (self.player, self.first_name, self.last_name)


class PlayerContract(models.Model):
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    shirt_number = models.PositiveSmallIntegerField(blank=True, default=0)

    def __unicode__(self):
        return u'%s in %s (%s)' % (self.player, self.club, self.from_date)


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
    LEAGUE = 'L'
    CUP = 'C'
    TYPE_CHOICES = (
        (LEAGUE, 'League'),
        (CUP, 'Cup')
        )
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=3)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    #level = models.PositiveSmallIntegerField(default=1)
    #seasons = models.ManyToManyField(Season, through='CompetitionSeason')


class CompetitionSeason(models.Model):
    competition = models.ForeignKey(Competition)
    season = models.ForeignKey(Season)
    start_date = models.DateField()
    end_date = models.DateField()
    has_playoff = models.BooleanField()

    class Meta:
        unique_together = ('competition', 'season')


class Round(models.Model):
    pass


class Match(models.Model):
    home_team = models.ForeignKey(Club, related_name='home_matches')
    away_team = models.ForeignKey(Club, related_name='away_matches')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    refereeA = models.CharField(max_length=100, blank=True)
    refereeB = models.CharField(max_length=100, blank=True)

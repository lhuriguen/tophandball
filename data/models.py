from django.db import models


# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3)
    country = models.CharField(max_length=3)
    ehf_id = models.IntegerField()
    address = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)


class Season(models.Model):
    year_from = models.PositiveSmallIntegerField()
    year_to = models.PositiveSmallIntegerField()


class ClubNames(models.Model):
    club = models.ForeignKey(Club)
    season = models.ForeignKey(Season)
    name = models.CharField(max_length=100)


class Player(models.Model):
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
        (WING, 'Wing')
        )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=3)
    #number = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=50, blank=True)
    height = models.PositiveSmallIntegerField(
        blank=True, help_text="Please indicate height in centimeters.")

    def is_back_player(self):
        return self.position in (
            self.LEFT_BACK, self.RIGHT_BACK, self.MIDDLE_BACK, self.BACK)


class PlayerNames(models.Model):
    player = models.ForeignKey(Player)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class PlayerContract(models.Model):
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)


class Coach(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=3)
    player = models.ForeignKey(Player, blank=True, null=True,
                               on_delete=models.SET_NULL)


class CoachContract(models.Model):
    coach = models.ForeignKey(Coach)
    club = models.ForeignKey(Club)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)

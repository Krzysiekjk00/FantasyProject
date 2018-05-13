from django.contrib.auth.models import User
from django.db import models

# Create your models here.



POSITIONS = (
    (1, 'Bramkarz'),
    (2, "Obrońca"),
    (3, "Pomocnik"),
    (4, "Napastnik")
)

ACTIVITY_POSITIONS = (
    (1, 'Bramkarz'),
    (2, "Obrońca"),
    (3, "Pomocnik"),
    (4, "Napastnik"),
    (5, "Wszyscy")
)

class Players(models.Model):
    name = models.CharField(max_length=64, verbose_name='Imię i Nazwisko')
    position = models.IntegerField(choices=POSITIONS, verbose_name='Pozycja', null=True)
    team = models.ForeignKey('Realteam', related_name='players', verbose_name='Zespół', null=True)
    activities = models.ManyToManyField('Activities', related_name='player_activity',
                                        verbose_name='Punktowanie czynności', null=True)
    overall_points = models.IntegerField(verbose_name='Suma punktów', null=True)
    is_specific = models.NullBooleanField(default=False, verbose_name='Czy jest "specificzny"?')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Zawodnik'
        verbose_name_plural = 'Zawodnicy'
        ordering = ['position']

class Activities(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa')
    point_value = models.IntegerField(verbose_name='Wartość punktowa', default=0)
    # position = models.IntegerField(choices=ACTIVITY_POSITIONS, verbose_name='dot_pozycji', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Czynność'
        verbose_name_plural = 'Czynności'

class RealTeam(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Rzeczywisty zespół'
        verbose_name_plural = 'Rzeczywiste zespoły'

class FootballMatch(models.Model):
    date = models.DateField(verbose_name='Data', null=True)
    time = models.TimeField(verbose_name='Godzina', null=True)
    home_team_name = models.ForeignKey(RealTeam, related_name='as_host', verbose_name='Nazwa zespołu gospodarzy',
                                       null=True)
    away_team_name = models.ForeignKey(RealTeam,  related_name='as_guest', verbose_name='Nazwa zespołu gości',
                                       null=True)
    home_team_players = models.ManyToManyField(Players, related_name='played_as_host',
                                               verbose_name='Zawodnicy Gospodarzy', default=0)
    away_team_players = models.ManyToManyField(Players, related_name='played_as_guest', verbose_name='Zawodnicy Gości', default=0)
    home_team_goals  = models.IntegerField(verbose_name='Gole gospodarzy', default=0)
    away_team_goals = models.IntegerField(verbose_name='Gole Gości', default=0)
    # home_team_assists = models.IntegerField(verbose_name='Ilość goli gości', default=0)
    # away_team_assists = models.IntegerField(verbose_name='Ilość asyst gości', default=0)
    # home_yellow_cards = models.IntegerField(verbose_name='Ilość żółtych kartek gospodarzy', default=0)
    # away_yellow_cards = models.IntegerField(verbose_name='Ilość żółtych kartek gości', default=0)
    # home_red_cards = models.IntegerField(verbose_name='Ilość czerwonych kartek gospodarzy', default=0)
    # away_red_cards = models.IntegerField(verbose_name='Ilość czerwonych kartek gości', default=0)
    # home_substitutes = models.IntegerField(verbose_name='Ilość zmian gospodarzy', default=0)
    # away_substitutes = models.IntegerField(verbose_name='Ilość zmian gości', default=0)

    def __str__(self):
        return 'Kolejka {} {}: {} vs {}'.format(self.date, self.time, self.home_team_name, self.away_team_name)

    class Meta:
        verbose_name = 'Mecz'
        verbose_name_plural = 'Mecze'

class UserTeam(models.Model):
    user = models.ForeignKey(User, verbose_name='Użytkownik')
    name = models.CharField(max_length=64, verbose_name='Nazwa zespołu użytkownika')
    team_players = models.ManyToManyField(Players, verbose_name='Zawodnicy użytkownika')
    team_points = models.IntegerField(verbose_name='Punkty drużyny', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Zespół użytkownika'
        verbose_name_plural = 'Zespoły użytkowników'











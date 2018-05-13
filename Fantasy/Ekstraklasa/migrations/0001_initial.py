# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-07 12:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Czynność',
                'verbose_name_plural': 'Czynności',
            },
        ),
        migrations.CreateModel(
            name='FootballMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='Termin')),
                ('home_team_goals', models.IntegerField(verbose_name='Gole gospodarzy')),
                ('away_team_goals', models.IntegerField(verbose_name='Gole Gości')),
            ],
            options={
                'verbose_name': 'Mecz',
                'verbose_name_plural': 'Mecze',
            },
        ),
        migrations.CreateModel(
            name='Gameweek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Kolejka')),
                ('matches', models.ManyToManyField(related_name='week', to='Ekstraklasa.FootballMatch', verbose_name='Mecze')),
            ],
            options={
                'verbose_name': 'Kolejka',
                'verbose_name_plural': 'Kolejki',
            },
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Imię i Nazwisko')),
                ('position', models.IntegerField(choices=[(1, 'Bramkarz'), (2, 'Obrońca'), (3, 'Pomocnik'), (4, 'Napastnik')], verbose_name='Pozycja')),
                ('last_game_points', models.IntegerField(verbose_name='Punkty w ostatniej kolejce')),
                ('overall_points', models.IntegerField(verbose_name='Suma punktów')),
                ('is_specific', models.BooleanField(default=False)),
                ('activities', models.ManyToManyField(related_name='player_activity', to='Ekstraklasa.Activities', verbose_name='Punktowanie czynności')),
            ],
            options={
                'verbose_name': 'Zawodnik',
                'verbose_name_plural': 'Zawodnicy',
            },
        ),
        migrations.CreateModel(
            name='RealTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Rzeczywisty zespół',
                'verbose_name_plural': 'Rzeczywiste zespoły',
            },
        ),
        migrations.CreateModel(
            name='User_Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa zespołu użytkownika')),
                ('team_players', models.ManyToManyField(to='Ekstraklasa.Players', verbose_name='Zawodnicy użytkownika')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name': 'Zespół użytkownika',
                'verbose_name_plural': 'Zespoły użytkowników',
            },
        ),
        migrations.AddField(
            model_name='players',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='Ekstraklasa.RealTeam', verbose_name='Zespół'),
        ),
        migrations.AddField(
            model_name='players',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_name',
            field=models.ManyToManyField(related_name='as_guest', to='Ekstraklasa.RealTeam', verbose_name='Nazwa zespołu gości'),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_players',
            field=models.ManyToManyField(related_name='played_as_guest', to='Ekstraklasa.Players', verbose_name='Zawodnicy Gości'),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='gameweek',
            field=models.ManyToManyField(related_name='match', to='Ekstraklasa.Gameweek', verbose_name='Kolejka'),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_name',
            field=models.ManyToManyField(related_name='as_host', to='Ekstraklasa.RealTeam', verbose_name='Nazwa zespołu gospodarzy'),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_players',
            field=models.ManyToManyField(related_name='played_as_host', to='Ekstraklasa.Players', verbose_name='Zawodnicy Gospodarzy'),
        ),
        migrations.AddField(
            model_name='activities',
            name='match',
            field=models.ManyToManyField(to='Ekstraklasa.FootballMatch', verbose_name='mecz'),
        ),
        migrations.AddField(
            model_name='activities',
            name='player',
            field=models.ManyToManyField(related_name='czynności', to='Ekstraklasa.Players', verbose_name='Zawodnik'),
        ),
    ]

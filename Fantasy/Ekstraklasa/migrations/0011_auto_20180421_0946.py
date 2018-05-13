# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-21 09:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ekstraklasa', '0010_activities_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footballmatch',
            name='away_team_name',
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_guest', to='Ekstraklasa.RealTeam', verbose_name='Nazwa zespołu gości'),
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='home_team_name',
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_host', to='Ekstraklasa.RealTeam', verbose_name='Nazwa zespołu gospodarzy'),
        ),
    ]

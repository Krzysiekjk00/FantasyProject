# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-21 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ekstraklasa', '0007_auto_20180421_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='userteam',
            name='team_points',
            field=models.IntegerField(default=0, verbose_name='Punkty drużyny'),
        ),
    ]

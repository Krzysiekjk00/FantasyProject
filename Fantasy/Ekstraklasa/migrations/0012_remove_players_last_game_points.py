# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-21 12:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ekstraklasa', '0011_auto_20180421_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='players',
            name='last_game_points',
        ),
    ]

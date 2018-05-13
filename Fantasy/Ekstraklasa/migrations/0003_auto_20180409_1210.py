# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-09 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ekstraklasa', '0002_auto_20180407_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='Ekstraklasa.RealTeam', verbose_name='Zespół'),
        ),
    ]
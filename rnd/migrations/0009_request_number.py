# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-28 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rnd', '0008_auto_20170828_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='number',
            field=models.CharField(default='0000', max_length=20),
        ),
    ]

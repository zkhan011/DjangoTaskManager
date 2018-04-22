# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-29 04:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rnd', '0011_auto_20170829_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='manager_approved',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Declined'), (2, 'Approved')], default=0),
        ),
        migrations.AlterField(
            model_name='request',
            name='owner_approved',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Declined'), (2, 'Approved')], default=0),
        ),
    ]
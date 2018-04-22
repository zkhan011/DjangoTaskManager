# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-29 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rnd', '0010_request_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='manager_approved',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Not Approved'), (2, 'Approved')], default=0),
        ),
    ]

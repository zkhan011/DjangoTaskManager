# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-07 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_auto_20171128_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundsrequest',
            name='payment_priority',
            field=models.IntegerField(default=0),
        ),
    ]

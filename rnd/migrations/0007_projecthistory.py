# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-20 11:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rnd', '0006_auto_20170820_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('designers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('lead_designer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rnd.Project')),
            ],
        ),
    ]

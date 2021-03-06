# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-01 06:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0003_fundsrequest_po'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receivables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('comments', models.TextField()),
                ('created', models.DateField(auto_now=True)),
                ('received', models.BooleanField(default=False)),
                ('number', models.CharField(default='', max_length=20)),
                ('partner', models.CharField(blank=True, max_length=150, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

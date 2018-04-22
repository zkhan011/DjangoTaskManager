# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-05 12:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0004_auto_20171204_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('pwo', models.CharField(blank=True, max_length=150, null=True)),
                ('start_date', models.DateField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_project_assignee', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.Department')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_project_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-28 05:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rnd', '0007_projecthistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required_date', models.DateField()),
                ('text', models.TextField()),
                ('created', models.DateField(auto_now=True)),
                ('manager_approved', models.BooleanField(default=False)),
                ('owner_approved', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField()),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rnd.Request')),
            ],
        ),
        migrations.AddField(
            model_name='model',
            name='in_work',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rnd.Model'),
        ),
    ]
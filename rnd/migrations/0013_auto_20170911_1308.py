# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-11 09:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rnd', '0012_auto_20170829_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestApprovalLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(choices=[(0, 'Pending'), (1, 'Declined'), (2, 'Approved')], default=0)),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rnd.Request')),
            ],
        ),
        migrations.RemoveField(
            model_name='requestapproval',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='requestapproval',
            name='request',
        ),
        migrations.DeleteModel(
            name='RequestApproval',
        ),
    ]

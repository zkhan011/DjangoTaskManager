# coding: UTF-8
# Copyright: Dmitriy Antonenko 2017

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PRIORITY_TYPES = ((10, 'Low'),
                  (20, 'Medium'),
                  (30, 'High'),
                  (40, 'Top Urgent'),)

class ActionType(models.Model):
    """
    Permissions Type
        Can Edit Bookings  1504
        ...
    """
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=50)  # для облегчения поиска и группировки
    code = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']
        verbose_name_plural = u"Action Types"

    def __unicode__(self):
        return self.name


class UserRole(models.Model):
    """
    User roles in system
        Engineer
        Manager
        etc
    """
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(ActionType)

    class Meta:
        ordering = ['name']
        verbose_name_plural = u"User Roles"

    def __unicode__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserProfile(models.Model):
    """
    User Profile model to save additional company-related and system information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    department = models.ForeignKey(Department, blank=True, null=True)
    # action access system
    roles = models.ManyToManyField(UserRole)
    direct_access = models.ManyToManyField(ActionType, blank=True)

    class Meta:
        ordering = ['user']
        verbose_name_plural = u"User Profiles"

    def _get_roles_list(self):
        """
        :return: List of Roles assigned to user
        """
        roles_list = ''
        for d in self.roles.all():
            roles_list += d.name + ", "
        return roles_list
    roles_list = property(_get_roles_list)


class SystemLog(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    dated = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=150, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    page = models.CharField(max_length=150, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    ip = models.CharField(max_length=20,  blank=True, null=True)
    level = models.CharField(max_length=20,  blank=True, null=True)


class Project(models.Model):
    code = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=150,)
    pwo = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)  # location
    owner = models.ForeignKey(User, blank=True, null=True, related_name='user_project_owner')
    assignee = models.ForeignKey(User, blank=True, null=True, related_name='user_project_assignee')
    status = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    units_total = models.IntegerField(blank=True, null=True)
    unit_completed = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    number = models.CharField(max_length=20, default='') #17-12-00005
    owner = models.ForeignKey(User, blank=True, null=True, related_name='user_task_owner')
    details = models.CharField(max_length=500)
    assignee = models.ForeignKey(User, blank=True, null=True, related_name='user_task_assignee')
    target_completion_date = models.DateField(blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)

    STATUS_TYPE = (('NS', 'Not Started'),
                   ('PR', 'Progress'),
                   ('BL', 'On Hold'),  # was "Blocked" before
                   ('CM', 'Completed'),
                   ('CC', 'Cancelled'),  # new status, GG asked to add
                   ('FD', 'Failed'),  # new status, GG asked to add
                   )
    status = models.CharField(max_length=2, choices=STATUS_TYPE, default='NS')
    # department = models.CharField(max_length=30, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, blank=True, null=True) # Project, task related to
    priority = models.IntegerField(choices=PRIORITY_TYPES, default=10)

    def __unicode__(self):
        return self.number


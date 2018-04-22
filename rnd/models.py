# coding: UTF-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

APPROVAL_TYPES = ((0, 'Pending'),
                  (1, 'Declined'),
                  (2, 'Approved'),
                  (3, 'Completed'),
                  )


class Model(models.Model):
    name = models.CharField(max_length=200)
    index = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User)  # created by
    created = models.DateField()
    files_path = models.CharField(max_length=500, null=True, blank=True)
    files_qty = models.IntegerField(null=True, blank=True)
    in_work = models.BooleanField(default=False)  # TRUE if model is used by someone, to avoid double issue

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.encode('utf8')


class Project(models.Model): # Models in work
    name = models.CharField(max_length=200)
    required_models = models.ManyToManyField(Model)
    lead_designer = models.ForeignKey(User)
    due_date = models.DateField()
    #start_date = models.DateField()
    #end_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name.encode('utf8')


class ProjectHistory(models.Model):
    project = models.ForeignKey(Project)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    #designer = models.ForeignKey(User)
    lead_designer = models.ForeignKey(User, related_name='+')
    designers = models.ManyToManyField(User, blank=True)


class ModelHistory(models.Model):
    model = models.ForeignKey(Model)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    designer = models.ForeignKey(User)


class Request(models.Model):
    author = models.ForeignKey(User)
    required_date = models.DateField()
    model = models.ForeignKey(Model, null=True)
    number = models.CharField(max_length=20, default='0000')
    text = models.TextField()
    created = models.DateField(auto_now=True)
    #manager_approved = models.BooleanField(default=False)
    manager_approved = models.IntegerField(choices=APPROVAL_TYPES, default=0)
    owner_approved = models.IntegerField(choices=APPROVAL_TYPES, default=0)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.number.encode('utf8')


class RequestApprovalLog(models.Model):
    request = models.ForeignKey(Request)
    #approved = models.BooleanField()  # can be TRUE or FALSE, approved and not approved
    result = models.IntegerField(choices=APPROVAL_TYPES, default=0)
    comments = models.CharField(max_length=500, blank=True, null=True)
    approved_by = models.ForeignKey(User)
    dated = models.DateTimeField(auto_now_add=True)





# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
APPROVAL_TYPES = ((0, 'Pending'),
                  (1, 'Declined'),
                  (2, 'Approved'),
                  (3, 'Completed'),
                  )
PRIORITY_TYPES = ((10, 'Low'),
                  (20, 'Medium'),
                  (30, 'High'),
                  (40, 'Top Urgent'),
                  (50, 'Someone are dying'))


class PaymentMode(models.Model):
    number = models.CharField(max_length=20)
    #name = models.CharField(max_length=20)

    def __str__(self):
        return self.number.encode('utf8')


class FundsRequest(models.Model):
    author = models.ForeignKey(User)
    created = models.DateField(auto_now_add=True)
    required_date = models.DateField()
    number = models.CharField(max_length=20, default='00000')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in AED
    comments = models.TextField()
    project = models.CharField(max_length=100, null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITY_TYPES, default=10)
    approved = models.IntegerField(choices=APPROVAL_TYPES, default=0)
    completed = models.BooleanField(default=False)
    po = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.CharField(max_length=200, null=True, blank=True)
    payment_mode = models.ForeignKey(PaymentMode, null=True, blank=True)

    payment_priority = models.IntegerField(default=0)

    def __str__(self):
        return self.number.encode('utf8')


class FundsRequestApprovalLog(models.Model):
    request = models.ForeignKey(FundsRequest)
    #approved = models.BooleanField()  # can be TRUE or FALSE, approved and not approved
    result = models.IntegerField(choices=APPROVAL_TYPES, default=0)
    comments = models.CharField(max_length=500, blank=True, null=True)
    approved_by = models.ForeignKey(User)
    dated = models.DateTimeField(auto_now_add=True)


class Receivables(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in AED
    date = models.DateField()  # expected date
    comments = models.TextField()
    author = models.ForeignKey(User)
    created = models.DateField(auto_now=True)
    received = models.BooleanField(default=False)
    number = models.CharField(max_length=20, default='')
    partner = models.CharField(max_length=150, blank=True, null=True)




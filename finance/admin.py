# coding: utf-8

from django.contrib import admin
from finance.models import *

# Register your models here.


@admin.register(FundsRequest)
class FundsRequestAdmin(admin.ModelAdmin):
    list_display = ('number', 'required_date', 'amount', 'po',  'completed', 'author', 'created')
    search_fields = ('number',)


@admin.register(Receivables)
class ReceivablesAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'amount', 'partner', 'author', 'created')
    search_fields = ('number',)


@admin.register(PaymentMode)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ('number',)


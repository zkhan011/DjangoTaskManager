# coding: utf-8

from django.contrib import admin
from rnd.models import *

# Register your models here.



@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'index', 'author', 'created')
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'lead_designer', 'due_date', 'completed')
    search_fields = ('name',)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('number', 'author', 'required_date', 'created', 'model', 'manager_approved', 'owner_approved',
                    'completed', 'deleted')
    search_fields = ('number', 'id')



@admin.register(RequestApprovalLog)
class RequestApprovalLogAdmin(admin.ModelAdmin):
    list_display = ('request', 'result', 'comments', 'approved_by', 'dated')


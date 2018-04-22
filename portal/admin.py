#coding: utf-8
# Copyright: Dmitriy Antonenko 2017

from django.contrib import admin

from models import *
from streit.settings import PROJECT_NAME
from django.contrib.auth.admin import UserAdmin


# Register your models here.
# change header in Admin panel
admin.site.site_title = "%s administration" % PROJECT_NAME
admin.site.site_header = "%s administration" % PROJECT_NAME

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff', 'last_login', 'id')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('dated', 'user', 'action', 'page', 'url', 'ip', 'level')
    list_filter = ('dated', 'user')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roles_list')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', )


@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code')
    list_display = ('name', 'group', 'code', 'id')
    list_filter = ('group', )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('number', 'owner', 'assignee', 'status', 'start_date', 'target_completion_date', 'completion_date', 'completed')
    search_fields = ('number', )
    list_filter = ('owner', 'assignee')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'pwo', 'start_date', 'due_date', 'owner', 'assignee', 'status', 'completed' )
    search_fields = ('name', )
    list_filter = ('owner', 'assignee', 'completed')




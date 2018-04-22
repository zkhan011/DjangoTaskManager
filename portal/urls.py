# coding: UTF-8
# Copyright: Dmitriy Antonenko 2017

# Portal App URLs

from django.conf.urls import url

import views as v

urlpatterns = [

    # Tasks
    url(r'tasks/list/?$', v.tasks_list),
    url(r'tasks/list/completed/?$', v.tasks_list_completed),
    url(r'tasks/list/canceled/?$', v.tasks_list_canceled),


    url(r'tasks/create/?$', v.tasks_create),
    url('tasks/(?P<tid>[0-9]*)/details/?$', v.tasks_details),

    url('tasks/dashboard/?$', v.tasks_dashboard),
    url('tasks/dashboard_new/?$', v.tasks_dashboard_new),

    url(r'projects/list/?$', v.projects_list),
    url(r'projects/create/?$', v.projects_create),
    url('projects/(?P<pid>[0-9]*)/details/?$', v.projects_details),


    url('task/ajax/edit/(?P<tid>[0-9]*)/?$', v.ajax_task_edit),

    url('tasks/report/?$', v.task_report),

    url('tasks/reports/(?P<name>[a-z0-9]{2,10})/?$', v.task_reports),

    url(r'test/mail?$', v.mail_test),
]

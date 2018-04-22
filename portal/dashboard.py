# coding: UTF-8
# Copyright: Dmitriy Antonenko 2017

from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .models import Task


def personal_tasks(request):

    user_tasks = Task.objects.filter(completed=False).filter(assignee=request.user)
   
    tasks = dict()
    tasks['total'] = user_tasks.count()
    tasks['progress'] = user_tasks.filter(status__exact='PR').count()
    tasks['completed'] = user_tasks.filter(status__exact='CM').count()
    tasks['blocked'] = user_tasks.filter(status__exact='BL').count()
    tasks['not_started'] = user_tasks.filter(status__exact='NS').count()
    tasks['failed'] = user_tasks.filter(status__exact='FD').count()
    tasks['canceled'] = user_tasks.filter(status__exact='CC').count()
    tasks['priority'] = user_tasks.filter(priority__lte=40).count()
    tasks['pcomplete'] = user_tasks.filter(status__exact='CM').filter(priority=40).count()
    tasks['pcanceled'] = user_tasks.filter(status__exact='CC').filter(priority=40).count()
    tasks['pblocked'] = user_tasks.filter(status__exact='BL').filter(priority=40).count()
    if  tasks['priority'] - tasks['pcanceled']:
        tasks['priorityperformance'] = float(tasks['pcomplete']) / ( tasks['priority'] - tasks['pcanceled'] - tasks['pblocked']) * 100.0
    else:
        tasks['priorityperformance'] = 0  

    if tasks['total'] - tasks['canceled']:
        tasks['performance'] = float(tasks['completed']) / (tasks['total'] - tasks['canceled'] - tasks['blocked'] ) * 100.0
    else:
        tasks['performance'] = 0

    return render_to_string('portal/portal/dashboards/personal_tasks_status.html', {'user': request.user,
                                                                                    'tasks': tasks})


def total_tasks(request):

    total_tasks = Task.objects.filter(completed=False)
   
    #users = total_tasks.distinct('assignee')
    users_id = total_tasks.values('assignee').distinct()
    #users = total_tasks.values_list('assignee').distinct()

    data = []
    record = dict()


    # [{'assignee': 8}, {'assignee': 1}]

    for r in users_id:
        user = User.objects.get(id=r['assignee'])
        record['user'] = user

        user_tasks = Task.objects.filter(completed=False).filter(assignee=user)

        record['total'] = user_tasks.count()
        record['progress'] = user_tasks.filter(status__exact='PR').count()
        record['completed'] = user_tasks.filter(status__exact='CM').count()
        record['blocked'] = user_tasks.filter(status__exact='BL').count()
        record['not_started'] = user_tasks.filter(status__exact='NS').count()
        record['failed'] = user_tasks.filter(status__exact='FD').count()
        record['canceled'] = user_tasks.filter(status__exact='CC').count()
        record['priority'] = user_tasks.filter(priority=40).count()
        record['pcomplete'] = user_tasks.filter(status__exact='CM').filter(priority=40).count()
        record['pcanceled'] = user_tasks.filter(status__exact='CC').filter(priority=40).count()
        record['pblocked'] = user_tasks.filter(status__exact='BL').filter(priority=40).count()
        if  record['priority']:
            record['priorityperformance'] = float(record['pcomplete']) / (record['priority'] - record['pcanceled'] - record['pblocked']) * 100.0  
        else:
            record['priorityperformance'] = 0 
          
        if record['total'] - record['canceled']:
            record['performance'] = float(record['completed']) / (record['total'] - record['canceled'] - record['blocked'] ) * 100.0
        else:
            record['performance'] = 0

        data.append(record)
        record = {}


    #tasks = dict()
    # tasks['total'] = user_tasks.count()
    # tasks['progress'] = user_tasks.filter(status__exact='PR').count()
    # tasks['completed'] = user_tasks.filter(status__exact='CM').count()
    # tasks['blocked'] = user_tasks.filter(status__exact='BL').count()
    # tasks['not_started'] = user_tasks.filter(status__exact='NS').count()

    #users = None

    return render_to_string('portal/portal/dashboards/total_tasks_status.html', {'data': data, 'users': users_id})

def total_tasks_new(request):

    total_tasks = Task.objects.filter(completed=False)

    #users = total_tasks.distinct('assignee')
    users_id = total_tasks.values('assignee').distinct()
    #users = total_tasks.values_list('assignee').distinct()

    data = []
    record = dict()


    # [{'assignee': 8}, {'assignee': 1}]

    for r in users_id:
        user = User.objects.get(id=r['assignee'])
        record['user'] = user

        user_tasks = Task.objects.filter(completed=False).filter(assignee=user)

        record['total'] = user_tasks.count()
        record['totalmid'] = user_tasks.filter(priority=20).count()
        record['totalhigh'] = user_tasks.filter(priority=30).count()
        record['totaltop'] = user_tasks.filter(priority=40).count()
        record['totallow'] = user_tasks.filter(priority=10).count() 
        record['midblocked'] = user_tasks.filter(status__exact='BL').filter(priority=20).count()
        record['highblocked'] = user_tasks.filter(status__exact='BL').filter(priority=30).count()
        record['topblocked'] = user_tasks.filter(status__exact='BL').filter(priority=40).count()
        record['lowblocked'] = user_tasks.filter(status__exact='BL').filter(priority=10).count()
        record['midcanceled'] = user_tasks.filter(status__exact='CC').filter(priority=20).count()
        record['highcanceled'] = user_tasks.filter(status__exact='CC').filter(priority=30).count()
        record['topcanceled'] = user_tasks.filter(status__exact='CC').filter(priority=40).count()
        record['lowcanceled'] = user_tasks.filter(status__exact='CC').filter(priority=10).count()

        record['progress'] = user_tasks.filter(status__exact='PR').count()
        record['completed'] = user_tasks.filter(status__exact='CM').count()
        record['blocked'] = user_tasks.filter(status__exact='BL').count()
        record['not_started'] = user_tasks.filter(status__exact='NS').count()
        record['failed'] = user_tasks.filter(status__exact='FD').count()
        record['canceled'] = user_tasks.filter(status__exact='CC').count()
        record['priority'] = user_tasks.filter(priority=40).count()
        record['pcomplete'] = user_tasks.filter(status__exact='CM').filter(priority=40).count()
        record['pcanceled'] = user_tasks.filter(status__exact='CC').filter(priority=40).count()
        record['pblocked'] = user_tasks.filter(status__exact='BL').filter(priority=40).count()
        
        if  record['priority']:
            record['priorityperformance'] = float(record['pcomplete']) / (record['priority'] - record['pcanceled'] - record['pblocked']) * 100.0
        else:
            record['priorityperformance'] = 0

        if record['total'] - record['canceled']:
            record['performance'] = float(record['completed']) / (record['total'] - record['canceled'] - record['blocked'] ) * 100.0
            record['performance'] = 0

        data.append(record)
        record = {}


    #tasks = dict()
    # tasks['total'] = user_tasks.count()
    # tasks['progress'] = user_tasks.filter(status__exact='PR').count()
    # tasks['completed'] = user_tasks.filter(status__exact='CM').count()
    # tasks['blocked'] = user_tasks.filter(status__exact='BL').count()
    # tasks['not_started'] = user_tasks.filter(status__exact='NS').count()

    #users = None

    return render_to_string('portal/portal/dashboards/total_tasks_status_new.html', {'data': data, 'users': users_id})


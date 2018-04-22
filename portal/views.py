# coding: UTF-8
# Copyright: Dmitriy Antonenko 2017


from django.shortcuts import render
from django.template.response import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from portal.functions import get_user_permissions, syslog, can_do
from .forms import *
from django.db import models
import dashboard
from portal.models import Task, Project

from datetime import datetime


def index(request):
    # return HttpResponse('index page')
    if request.user.is_authenticated():
        dashboard_tasks = dashboard.personal_tasks(request)

        return render(request, 'portal/index.html', {'dashboard_tasks': dashboard_tasks,
                                                     })
    else:
        return render(request, 'portal/index_not_logged.html', {})


@login_required
def rnd(request):
    #
    return HttpResponse('RnD')


def support(request):
    return render(request, 'portal/support.html', {})


@login_required
def search(request):
    return render(request, 'portal/search.html', {})


@login_required
def user_settings(request):
    permissions = get_user_permissions(request.user)
    return render(request, 'portal/user_settings.html', {'permissions': permissions})


@login_required
def tasks_create(request):
    """
    Create a new task

    :param request:
    :return:
    """

    if not can_do(request.user, 1810):  # Tasks. Can create/assign tasks
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1810)'})

    project_id = request.GET.get('project', '')
    project = None
    if project_id:
        try:
            project = Project.objects.get(id=project_id)
        except models.ObjectDoesNotExist:
            project = None

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateTaskForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            task.number = task.start_date.strftime('%y-%m-') + str(task.id).zfill(4)
            task.save()

            syslog(request, action='Added new Task #%s' % task.number)

            if project:
                return HttpResponseRedirect('projects/%s/details' % project.id)
            else:
                return HttpResponseRedirect('/tasks/list')

    # if a GET (or any other method) we'll create a blank form
    else:
        if project:
            form = CreateTaskForm(initial={'project': project})
        else:
            form = CreateTaskForm()

    return render(request, 'portal/portal/task_create.html', {'form': form})


@login_required
def tasks_list(request):
    """

    :param request:
    :return: list of filtered tasks
    """
    can_manage = False

    assignee_id = request.GET.get('assignee', '')
    owner_id = request.GET.get('owner', '')
    assignee = None
    owner = None
    filter = False

    # params_string = request.META['QUERY_STRING']

    if can_do(request.user, 1810):  # Tasks. Can create/assign tasks

        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
            except models.ObjectDoesNotExist:
                assignee = None

        if owner_id:
            try:
                owner = User.objects.get(id=owner_id)
            except models.ObjectDoesNotExist:
                owner = None

        if assignee:
            tasks = Task.objects.filter(completed=False).filter(assignee=assignee).order_by('id')
            filter = True
        elif owner:
            tasks = Task.objects.filter(completed=False).filter(owner=owner).order_by('id')
            filter = True
        else:
            tasks = Task.objects.filter(completed=False).order_by('id')

        can_manage = True
        completed_tasks = Task.objects.filter(completed=True)
    else:
        tasks = Task.objects.filter(completed=False).filter(assignee=request.user)
        completed_tasks = Task.objects.filter(completed=True).filter(assignee=request.user)

    today = datetime.now()

    return render(request, 'portal/portal/task_list.html', {'tasks': tasks.exclude(status='CC'), 'can_manage': can_manage,
                                                            'completed_tasks': completed_tasks,
                                                            'filter': filter, 'today': today,
                                                            'owner': owner, 'assignee': assignee})


def tasks_list_completed(request):
    completed_tasks = None
    can_manage = False

    if can_do(request.user, 1810):  # Tasks. Can create/assign tasks
        can_manage = True
        completed_tasks = Task.objects.filter(completed=True)
    else:
        completed_tasks = Task.objects.filter(completed=True).filter(assignee=request.user)

    return render(request, 'portal/portal/task_list_completed.html', {'completed_tasks': completed_tasks, })


def tasks_list_canceled(request):
    tasks = None
    can_manage = False

    if can_do(request.user, 1810):  # Tasks. Can create/assign tasks
        can_manage = True
        tasks = Task.objects.filter(status='CC')
    else:
        tasks = Task.objects.filter(assignee=request.user).filter(status='CC')

    return render(request, 'portal/portal/task_list_canceled.html', {'tasks': tasks, })



@login_required
def tasks_details(request, tid):
    """
    Show / Edit Task details
    Select form depends of Task owner
    :param request:
    :param tid:
    :return:

    как Django передает параметры фильтров
    http://127.0.0.1:8000/admin/portal/task/8/change/?_changelist_filters=owner__id__exact%3D7%26assignee__id__exact%3D1

    """
    try:
        task = Task.objects.get(id=tid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Record does not exist!'})

    # getting used filter from GET params
    pfilter = request.GET.get('_filter', '')

    if request.user == task.assignee:
        selected_form = AssigneeEditTaskForm
    elif request.user == task.owner or can_do(request.user, 1810):
        selected_form = OwnerEditTaskForm  # can edit all fields in Task
    else:
        form = None
        return render(request, 'portal/portal/task_details.html', {'task': task, 'form': form})

    if request.method == 'POST':
        # form = AssigneeEditTaskForm(request.POST, instance=task)
        form = selected_form(request.POST, instance=task)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()

            syslog(request, action='Updated Task #%s' % task.number)

            if filter:
                return HttpResponseRedirect('/tasks/list?%s' % pfilter)
            else:
                return HttpResponseRedirect('/tasks/list/')
    else:
        # form = AssigneeEditTaskForm(instance=task)
        form = selected_form(instance=task)

    return render(request, 'portal/portal/task_details.html', {'task': task, 'form': form})


@login_required
def projects_list(request):
    """
    Show Projects list
    :param request:
    :return:
    """

    projects = Project.objects.all()

    can_manage = True
    return render(request, 'portal/portal/project_list.html', {'projects': projects, 'can_manage': can_manage})


@login_required
def projects_create(request):
    if not can_do(request.user, 1820):  # Tasks. Can create/assign projects
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1820)'})

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateProjectForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.code = "PR" + str(project.id).zfill(
                4)  # task.start_date.strftime('%y-%m-') + str(project.id).zfill(4)
            project.save()

            syslog(request, action='Added new Project #%s' % project.code)
            return HttpResponseRedirect('/projects/list')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateProjectForm()

    return render(request, 'portal/portal/project_create.html', {'form': form})


@login_required
def projects_details(request, pid):
    can_manage = False
    if can_do(request.user, 1820):  # Tasks. Can Manage projects
        can_manage = True
        # return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1821)'})

    try:
        project = Project.objects.get(id=pid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Record does not exist!'})

    tasks = Task.objects.filter(project=project).order_by('start_date')

    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            syslog(request, action='Updated Project #%s' % project.code)
            return HttpResponseRedirect('/projects/list/')
    else:
        form = EditProjectForm(instance=project)

    return render(request, 'portal/portal/project_details.html', {'project': project, 'form': form,
                                                                  'can_manage': can_manage, 'tasks': tasks})


@login_required
def tasks_dashboard(request):
    total_tasks = dashboard.total_tasks(request)

    return render(request, 'portal/portal/task_dashboard.html', {'total_tasks': total_tasks})

@login_required
def tasks_dashboard_new(request):
    total_tasks_new = dashboard.total_tasks_new(request)
   
    return render(request, 'portal/portal/task_dashboard_new.html', {'total_tasks_new': total_tasks_new})





def mail_test(request):
    # from django.core.mail import EmailMessage
    # email = EmailMessage('Test 2', 'World 123 123 234 ', to=['dmitriy.antonenko@armored-cars.com'])
    # email.send()

    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from datetime import datetime

    params = None

    # msg_plain = render_to_string('vms/qc/lines_status_email.txt', {'params': params})

    now = datetime.now()

    # report = calculate_production_percentage
    # msg_html = render_to_string('vms/qc/lines_status_email.html', {'records': report, 'now': now})

    msg_html = 'Email body   <a href="http://127.0.0.1:8000/tasks/5/details ">  details </a>'

    subject = now.strftime('Portal status for %H:%M, %Y-%m-%d')
    msg_plain = subject

    send_mail(
        subject,
        msg_plain,
        'streit.portal@armoured-cars.com',  # from
        #  ['dmitriy.antonenko@armored-cars.com',], # to
        ['it@armored-cars.com'],

        html_message=msg_html,

        fail_silently=False,
    )
    return HttpResponse('Email sent')

    # return render(request, 'vms/info.html', {'message': 'Email sent'})


def send_task_notification_email(id):
    """
    Send email-notification to Task Assignee
    :param id:  Task ID
    :return:
    """
    task = Task.objects.get(id=id)


def ajax_task_edit(request, tid):
    # https://teamtreehouse.com/community/keep-a-modal-window-open-after-form-submission
    # https://dmorgan.info/posts/django-views-bootstrap-modals/
    # ! https://stackoverflow.com/questions/11276100/how-do-i-insert-a-django-form-in-twitter-bootstrap-modal-window

    try:
        task = Task.objects.get(id=tid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Record does not exist!'})

    selected_form = None

    # Edit tasks logic
    if request.user == task.owner: #or can_do(request.user, 1810):
        selected_form = OwnerEditTaskForm  # can edit all fields in Task
        edit_privilege = 'owner'
    elif request.user == task.assignee:
        selected_form = AssigneeEditTaskForm
        edit_privilege = 'assignee'
        if can_do(request.user, 1832):  # Tasks. Can Edit Tasks Assigned to Yourself
            selected_form = OwnerEditTaskForm  # can edit all fields in Task
            edit_privilege = 'owner'
    elif can_do(request.user, 1830):  # Tasks. Can Edit Others` Tasks
            selected_form = OwnerEditTaskForm  # can edit all fields in Task
            edit_privilege = 'owner'

    else:
        edit_privilege = 'read'
        return render(request, 'portal/portal/ajax/task_ajax_form.html', {'task': task, 'form': selected_form,
                                                                          'edit_privilege': edit_privilege})

    #if can_do(request.user, 1830):  # Tasks. Can Edit Others` Tasks
    #    selected_form = OwnerEditTaskForm  # can edit all fields in Task
    #    edit_privilege = 'owner'

    if request.method == 'POST':
        form = selected_form(request.POST, instance=task)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form
            form.save()
            syslog(request, action='Updated Task #%s' % task.number)
            # return HttpResponse('Updated')
            return render(request, 'portal/portal/ajax/task_list_tr_row.html', {'t': task})
    else:
        # form = AssigneeEditTaskForm(instance=task)
        form = selected_form(instance=task)

    return render(request, 'portal/portal/ajax/task_ajax_form.html', {'task': task, 'form': form,
                                                                      'edit_privilege': edit_privilege
                                                                      })


def task_reports(request, name):
    if name == 'ytd':
        return render(request, 'portal/portal/reports/tasks_selected_report.html', {'name': name})

    return render(request, 'portal/error.html', {'error_message': 'Unknown report name!'})


def task_report(request):
    if not can_do(request.user, 1910):  # Reports
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1910)'})

    form = TasksReport()
    data = None
    total_tasks = None

    period = request.GET.get('period', '')

    if period:

        try:
            period = int(period)
        except:
            return render(request, 'portal/error.html', {'error_message': 'Param Error'})

        if period < 0 or period > 13:
            return render(request, 'portal/error.html', {'error_message': 'Param Error'})

        form = TasksReport(request.GET)
        if form.is_valid():
            today = datetime.now()
            last_month = today.month - 1 if today.month>1 else 12
            #last_month_year = today.year if today.month > last_month else today.year - 1
            #Order.objects.filter(created_at__year=last_month_year, created_at__month=last_month)
            current_month = today.month
            current_year = today.year

            if period == 0:
                period = current_month

            if period == 13:
                total_tasks = Task.objects.filter(target_completion_date__year=current_year)
            else:
                total_tasks = Task.objects.filter(target_completion_date__month=period)

            data = []
            record = dict()
            assignees = total_tasks.values('assignee').distinct()
            for r in assignees:
                user = User.objects.get(id=r['assignee'])
                record['user'] = user
                user_tasks = total_tasks.filter(assignee=user)
                record['total'] = user_tasks.count()
                record['progress'] = user_tasks.filter(status__exact='PR').count()
               # record['completed'] = user_tasks.filter(status__exact='CM').count()
                record['completed'] = user_tasks.filter(completed=True).count()
                record['blocked'] = user_tasks.filter(status__exact='BL').count() # On Hold
                record['not_started'] = user_tasks.filter(status__exact='NS').count()
                record['failed'] = user_tasks.filter(status__exact='FD').count()
                record['canceled'] = user_tasks.filter(status__exact='CC').count()

                if record['total'] - record['canceled']:
                    record['performance'] = float(record['completed']) / (record['total'] - record['canceled']) * 100.0
                else:
                    record['performance'] = 0

                data.append(record)
                record = {}

    return render(request, 'portal/portal/reports/tasks_report.html', {'form': form, 'data': data, 'total_tasks': total_tasks})

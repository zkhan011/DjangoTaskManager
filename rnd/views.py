# coding: UTF-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseRedirect

from rnd.models import Model, Project, Request, RequestApprovalLog
from rnd.forms import AddRequestForm
from portal.functions import syslog, can_do

# Create your views here.


@login_required
def projects(request):

    if not can_do(request.user, 1700):  # Can access RnD Actions
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1700)'})

    models = Model.objects.all()

    projects = Project.objects.filter(completed=False).order_by('due_date')

    return render(request, 'portal/rnd/projects.html', {'allmodels': models, 'projects': projects})


@login_required
def models_list(request):

    if not can_do(request.user, 1700):  # Can access RnD Actions
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1700)'})

    models = Model.objects.all()
    return render(request, 'portal/rnd/models.html', {'allmodels': models, })


@login_required
def project(request, id):

    if not can_do(request.user, 1700):  # Can access RnD Actions
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1700)'})

    try:
        project = Project.objects.get(id=id)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Unit does not exist!'})

    return render(request, 'portal/rnd/project.html', {'project': project})


@login_required
def model(request, id):

    if not can_do(request.user, 1700):  # Can access RnD Actions
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1700)'})

    try:
        model = Model.objects.get(id=id)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Model does not exist!'})

    return render(request, 'portal/rnd/model.html', {'model': model})


@login_required
def requests_list(request):
    # List of request belongs to current user or all requests for managers

    if not can_do(request.user, 1700):  # Can access RnD Actions
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1700)'})

    manager = can_do(request.user, 1505)
    chairman = can_do(request.user, 1506)

    completed_requests = None

    if manager or chairman:
        requests = Request.objects.filter(deleted=False).filter(completed=False).order_by('required_date')
    else:
        requests = Request.objects.filter(author=request.user).filter(deleted=False).filter(completed=False).order_by('required_date')
        completed_requests = Request.objects.filter(author=request.user).filter(deleted=False).filter(completed=True).order_by('required_date')

    return render(request, 'portal/rnd/requests_list.html', {'requests': requests, 'completed_requests': completed_requests,
                                                             'manager': manager, 'chairman': chairman})


@login_required
def request_create(request):

    if not can_do(request.user, 1700):  # Can access RnD Actions
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1700)'})

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddRequestForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            mrequest = form.save(commit=False)
            mrequest.author = request.user
            mrequest.save()
            mrequest.number = mrequest.required_date.strftime('%y%m') + str(mrequest.id).zfill(5)
            mrequest.save()

            syslog(request, action='Added new Request #%s' % mrequest.number)

            return HttpResponseRedirect('/rnd/requests')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddRequestForm()

    return render(request, 'portal/rnd/request_create.html', {'form': form})


@login_required
def request_details(request, rid):

    if not can_do(request.user, 1700):  # Can access RnD Actions
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1700)'})

    # shows request details
    try:
        requestObj = Request.objects.get(id=rid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Request does not exist!'})

    if request.method == 'POST':

        #id = request.POST.get('who', '')
        who = request.POST.get('who', '')
        result = request.POST.get('result', '')
        comments = request.POST.get('comments', '')

        # RESULT: (1, 'Declined'), (2, 'Approved')


        log = RequestApprovalLog(request=requestObj)

        if who == 'admin':
            if result == 'complete':
                requestObj.completed = True
                requestObj.save()
                log.result = 3  # completed
                log.comments = comments
                log.approved_by = request.user
                log.save()
                return HttpResponseRedirect("/rnd/requests")


        #log = RequestApprovalLog(request=requestObj)
        if who == 'manager':
            if result == 'approved':
                requestObj.manager_approved = 2
            elif result == 'declined':
                requestObj.manager_approved = 1
            log.result = requestObj.manager_approved
        elif who == 'owner':
            if result == 'approved':
                requestObj.owner_approved = 2
            elif result == 'declined':
                requestObj.owner_approved = 1
            log.result = requestObj.owner_approved



        log.comments = comments
        log.approved_by = request.user
        log.save()

    requestObj.save()

    manager = can_do(request.user, 1505)
    chairman = can_do(request.user, 1506)




    #if not can_do(request.user, 1450):  # Can Add Unit
    #    return render(request, 'vms/error.html', {'error_message': 'Access denied.  (Code: #1450)'})

    if not manager and not chairman:
        if requestObj.author != request.user:
            return render(request, 'portal/error.html', {'error_message': 'You can manage only your own requests!'})

    return render(request, 'portal/rnd/request_details.html', {'request': requestObj, 'manager': manager,
                                                               'chairman': chairman})


@login_required
def request_delete(request, rid):

    try:
        reqst = Request.objects.get(id=rid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Request does not exist!'})

    if reqst.author != request.user:
        return render(request, 'portal/error.html', {'error_message': 'You can delete only your own requests!'})

    reqst.deleted = True
    reqst.save()

    #return render(request, 'portal/rnd/request_delete.html', {})
    return HttpResponseRedirect('/rnd/requests')




# coding: UTF-8

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db import models
from portal.functions import syslog, can_do
from finance.models import FundsRequest, FundsRequestApprovalLog, Receivables
from finance.forms import AddFundsRequestForm, ReceivableForm

from datetime import datetime
from datetime import timedelta



@login_required
def request_list(request):
    if not can_do(request.user, 1605):  # Can access "Finance forecast"
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1605)'})

    completed_requests = None

    can_manage = can_do(request.user, 1610)

    if can_manage:
        requests = FundsRequest.objects.filter(completed=False).order_by('required_date')
        completed_requests = FundsRequest.objects.filter(completed=True).order_by('required_date')
    else:
        requests = FundsRequest.objects.filter(author=request.user).filter(completed=False).order_by('required_date')
        completed_requests = FundsRequest.objects.filter(author=request.user).filter(completed=True).order_by(
            'required_date')

    return render(request, 'portal/finance/request_list.html',
                  {'requests': requests, 'completed_requests': completed_requests,
                   'can_manage': can_manage})


@login_required
def request_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddFundsRequestForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            mrequest = form.save(commit=False)
            mrequest.author = request.user
            mrequest.save()
            mrequest.number = mrequest.required_date.strftime('%y%m') + str(mrequest.id).zfill(5)
            mrequest.save()

            syslog(request, action='Added new Request #%s' % mrequest.number)

            return HttpResponseRedirect('/finance/requests')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddFundsRequestForm()

    return render(request, 'portal/finance/request_create.html', {'form': form})


@login_required
def request_details(request, rid):
    # shows request details
    try:
        requestObj = FundsRequest.objects.get(id=rid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Request does not exist!'})

    if request.method == 'POST':
        # id = request.POST.get('who', '')
        # who = request.POST.get('who', '')
        result = request.POST.get('result', '')
        comments = request.POST.get('comments', '')

        # RESULT: (1, 'Declined'), (2, 'Approved')

        log = FundsRequestApprovalLog(request=requestObj)

        if result == 'complete':
            requestObj.completed = True
            requestObj.save()
            log.result = 3  # completed
            log.comments = comments
            log.approved_by = request.user
            log.save()
            return HttpResponseRedirect("/finance/requests")

        if result == 'approved':
            requestObj.approved = 2
        elif result == 'declined':
            requestObj.approved = 1
        log.result = requestObj.approved

        log.comments = comments
        log.approved_by = request.user
        log.save()

    requestObj.save()

    can_aprove = can_do(request.user, 1611)

    # if not can_do(request.user, 1450):  # Can Add Unit
    #    return render(request, 'vms/error.html', {'error_message': 'Access denied.  (Code: #1450)'})

    if not can_aprove:
        if requestObj.author != request.user:
            return render(request, 'portal/error.html', {'error_message': 'You can manage only your own requests!'})

    return render(request, 'portal/finance/request_details.html', {'request': requestObj, 'can_aprove': can_aprove, })


@login_required
def forecast(request):
    if not can_do(request.user, 1650):  # Can access "Finance forecast"
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1650)'})

    # C:\Users\Dimon\PycharmProjects\jupiter\_work\Charts\Chart.js\samples
    # combo-bar-line.html
    # make by Month!

    return render(request, 'portal/finance/forecast.html', {})


@login_required
def receivables_list(request):
    if not can_do(request.user, 1655):  # Can access "Can access "Income Forecast""
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1655)'})

    records = Receivables.objects.order_by('date')
    return render(request, 'portal/finance/receivables_list.html', {'records': records})


@login_required
def receivables_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReceivableForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            obj.number = 'R' + obj.date.strftime('%y%m') + str(obj.id).zfill(5)
            obj.save()

            syslog(request, action='Added new Request #%s' % obj.number)

            return HttpResponseRedirect('/finance/receivables')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReceivableForm()

    return render(request, 'portal/finance/receivables_create.html', {'form': form})


@login_required
def receivables_details(request, rid):

    try:
        obj = Receivables.objects.get(id=rid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Record does not exist!'})

    return render(request, 'portal/finance/receivables_details.html', {'object': obj, })


def payments_manage1(request):
    """

    Shows Receivables forecast by 4 weeks
    Shows Funds request by 4 weeks

    :param request:
    :return:
    """

    # Manage payments

    if not can_do(request.user, 1670):  # Can access "Can access "Income Forecast""
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1670)'})



    # need to find first passed Sunday (beginning of the week)
    today = datetime.today()
   #  for
    date_from = datetime.today()

    # searching for first passed Sunday
    for i in range(-6, 1):
        day = today + timedelta(days=i)
        if day.weekday() == 5:  # 6 = Sunday,  5=Saturday  # weekday returns Monday is 0 ... and Sunday is 6
            date_from = day
            break

    date_to = date_from + timedelta(weeks=4)

    week1 = (date_from + timedelta(weeks=1)).date()
    week2 = (date_from + timedelta(weeks=2)).date()
    week3 = (date_from + timedelta(weeks=3)).date()
    week4 = (date_from + timedelta(weeks=4)).date()


    data_receivables = []

    receivables = Receivables.objects.filter(received=False).filter(date__lte=date_to).order_by('date')

    for i in receivables:
        record = {}
        record['receivable'] = i

        if i.date < today.date():
            record['week'] = 0
        elif i.date <= week1:
            record['week'] = 1
            #week1_sum += r.amount
        elif i.date <= week2:
            record['week'] = 2
            #week2_sum += r.amount
        elif i.date <= week3:
            record['week'] = 3
            #week3_sum += r.amount
        else:
            record['week'] = 4
            #week4_sum += r.amount

        data_receivables.append(record)

    overdue_requests = FundsRequest.objects.filter(completed=False).filter(required_date__lt=date_from).order_by('required_date')

    requests = FundsRequest.objects.filter(completed=False).filter(required_date__gte=date_from).\
        filter(required_date__lte=date_to).order_by('required_date')

    data = []

    week1_sum = 0
    week2_sum = 0
    week3_sum = 0
    week4_sum = 0
    overdue_sum = 0

    for r in requests:
        record = {}
        record['request'] = r

        if r.required_date <= week1:
            record['week'] = 1
            week1_sum += r.amount
        elif r.required_date <= week2:
            record['week'] = 2
            week2_sum += r.amount
        elif r.required_date <= week3:
            record['week'] = 3
            week3_sum += r.amount
        else:
            record['week'] = 4
            week4_sum += r.amount

        data.append(record)
        #record = {}  #!!!!

    for r in overdue_requests:
        overdue_sum += r.amount

    week_sums = {'overdue': overdue_sum, 'week1': week1_sum, 'week2': week2_sum, 'week3': week3_sum, 'week4': week4_sum}

    # select FundsRequest for next 4 weeks

    # order by date

    # build a table

    return render(request, 'portal/finance/payments_manage1.html', {'date_from': date_from,
                                                                   'date_to': date_to,
                                                                   # 'requests': requests,
                                                                   'data_requests': data,
                                                                   'week1': week1,
                                                                   'week2': week2,
                                                                   'week3': week3,
                                                                   'week4': week4,
                                                                   'week_sums': week_sums,
                                                                   'overdue_requests': overdue_requests,
                                                                   'data_receivables': data_receivables,
                                                                   })


@login_required
def ajax_updaterequest(request):
    """
    Updating priority on payment request
    """

    if request.method == "POST":

        record_id = request.POST.get('id', '')
        priority = request.POST.get('priority', '')

        try:
            record = FundsRequest.objects.get(id=record_id)
        except models.ObjectDoesNotExist:
            return HttpResponse("Error")

        try:
            priority = int(priority)
        except :
            return HttpResponse("Error")

        record.payment_priority = priority
        record.save()

        return HttpResponse(priority)

    return HttpResponse("")


@login_required
def request_delete(request, rid):

    try:
        requestObj = FundsRequest.objects.get(id=rid)
    except models.ObjectDoesNotExist:
        return render(request, 'portal/error.html', {'error_message': 'Request does not exist!'})

    if request.user != requestObj.author :
        return render(request, 'portal/error.html', {'error_message': 'You can delete own requests only!'})

    requestObj.delete()

    return HttpResponseRedirect("/finance/requests")


@login_required
def payments_proceed(request, pid):

    if not can_do(request.user, 1670):  # Can manage payment requests
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1670)'})

    message = ""

    if request.method == "POST":
        # proceed with finishing requests
        message = "Select records to complete payment."
        ids = request.POST.getlist('selected_id', '')
        if ids:
            requests = FundsRequest.objects.filter(id__in=ids)
            for r in requests:
                r.completed = True
                r.save()
            message = "%s Request(s) were completed" % requests.count()

    requests = FundsRequest.objects.filter(completed=False).filter(payment_priority=pid)

    return render(request, 'portal/finance/proceed_payment.html', {'requests': requests,
                                                                   'pid': pid,
                                                                   'message': message
                                                                   })




@login_required
def payments_manage(request):
    """
    Modified version of Payments management

    :param request:
    :return:
    """

    if not can_do(request.user, 1670):  # Can access "Can manage payment requests""  # Manage payments
        return render(request, 'portal/error.html', {'error_message': 'Access denied.  (Code: #1670)'})

    # need to find first passed Sunday (beginning of the week)
    today = datetime.today()
    date_from = datetime.today()

    # searching for first passed Sunday
    for i in range(-6, 1):
        day = today + timedelta(days=i)
        if day.weekday() == 5:  # 6 = Sunday,  5=Saturday  # weekday returns Monday is 0 ... and Sunday is 6
            date_from = day
            break

    date_to = date_from + timedelta(weeks=4)

    week1 = (date_from + timedelta(weeks=1)).date()
    week2 = (date_from + timedelta(weeks=2)).date()
    week3 = (date_from + timedelta(weeks=3)).date()
    week4 = (date_from + timedelta(weeks=4)).date()


    data_receivables = []

    receivables = Receivables.objects.filter(received=False).filter(date__lte=date_to).order_by('date')

    for i in receivables:
        record = {}
        record['receivable'] = i

        if i.date < today.date():
            record['week'] = 0
        elif i.date <= week1:
            record['week'] = 1
            #week1_sum += r.amount
        elif i.date <= week2:
            record['week'] = 2
            #week2_sum += r.amount
        elif i.date <= week3:
            record['week'] = 3
            #week3_sum += r.amount
        else:
            record['week'] = 4
            #week4_sum += r.amount

        data_receivables.append(record)

        requests = FundsRequest.objects.filter(completed=False).filter(required_date__lte=date_to).order_by('required_date')  #.filter(required_date__gte=date_from)

        data = []

        for r in requests:
            record = {}
            record['request'] = r

            if r.required_date <= week1:
                record['week'] = 1
                #week1_sum += r.amount
            elif r.required_date <= week2:
                record['week'] = 2
                #week2_sum += r.amount
            elif r.required_date <= week3:
                record['week'] = 3
                #week3_sum += r.amount
            else:
                record['week'] = 4
                #week4_sum += r.amount

            data.append(record)
        #record = {}  #!!!!


    return render(request, 'portal/finance/payments_manage.html', {'data_receivables': data_receivables,
                                                                    'data_requests': data,
                                                                   })
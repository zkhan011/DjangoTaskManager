# coding: UTF-8

# Finance App URLs

from django.conf.urls import url

import views as v

urlpatterns = [

    url(r'requests/?$', v.request_list),
    url(r'request/create/?$', v.request_create),
    url(r'request/(?P<rid>[0-9]*)/details', v.request_details),

    url(r'receivables/?$', v.receivables_list),
    url(r'receivables/create/?$', v.receivables_create),
    url(r'receivables/(?P<rid>[0-9]*)/details', v.receivables_details),

    #url(r'report/4weeks/?$', v.report_4weeks),




    url(r'forecast/?$', v.forecast),

    url(r'ajax/updaterequest/?$', v.ajax_updaterequest),

    url(r'request/(?P<rid>[0-9]*)/delete/?$', v.request_delete),

    url(r'payments/manage1/?$', v.payments_manage1), # первая версия (разбита по неделям)
    url(r'payments/proceed/(?P<pid>[0-9]*)/?$', v.payments_proceed),

    url(r'payments/manage/?$', v.payments_manage),





]
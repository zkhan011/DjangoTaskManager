# coding: utf-8

from django import forms
from django.forms import ModelForm
from django.db import models
from finance.models import FundsRequest, Receivables, PRIORITY_TYPES, PaymentMode


class AddFundsRequestForm(ModelForm):
    required_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                  'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
                                    input_formats=('%Y-%m-%d',), required=True)
    comments = forms.CharField(required=True,
                               widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '5'}))
    project = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',
                                                                            'placeholder': 'Project reference, if any'}))
    priority = forms.ChoiceField(choices=PRIORITY_TYPES,
                                 widget=forms.Select(attrs={'class': 'form-control input-sm'}))
    # amount = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))
    amount = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': 'Amount in AED' }))

    po = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',
                                                                       'placeholder': 'PO number'}))

    vendor = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',
                                                                           'placeholder': 'Vendor name'}))

    payment_mode = forms.ModelChoiceField(queryset=PaymentMode.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=True)

    class Meta:
        model = FundsRequest
        exclude = ('author', 'number', 'created', 'approved', 'completed', 'payment_priority')



class ReceivableForm(ModelForm):

    amount = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': 'Amount in AED' }))

    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                  'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),input_formats=('%Y-%m-%d',), required=True)
    comments = forms.CharField(required=True,
                               widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '5'}))

    partner = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',
                                                                            'placeholder': 'Partner/Company'}))

    class Meta:
        model = Receivables
        exclude = ('author', 'number', 'created', 'received')
# coding: utf-8

from django import forms
from django.forms import ModelForm
from django.db import models

from rnd.models import Request, Model

# class AddUnitForm(ModelForm):
#     """
#         Add new Unit form
#     """
#     uid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ',
#                                                         'placeholder':'Enter Unique Unit ID'}))
#
#     status = forms.ModelChoiceField(queryset=UnitStatus.objects.filter(type=1),
#                                     widget=forms.Select(attrs={'class': 'form-control input-sm'}))
#
#     vin = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm',
#                                                         'placeholder': 'Enter vehicle VIN'}))

# class ChangeStatusForm(forms.Form):
#     status = forms.ModelChoiceField(queryset=UnitStatus.objects.filter(type=1).exclude(id__in=(11,14,15)),
#                                     widget=forms.Select(attrs={'class': 'form-control input-sm'}))


class AddRequestForm(ModelForm):
    model = forms.ModelChoiceField(queryset=Model.objects.all(),  widget=forms.Select(attrs={'class': 'form-control input-sm'}))
    required_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                  'placeholder': 'YYYY-MM-DD'},  format='%Y-%m-%d'),
                                    input_formats=('%Y-%m-%d',), required=True)
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '15'}))

    class Meta:
        model = Request
        exclude = ('author', 'number', 'created', 'manager_approved', 'owner_approved', 'completed')



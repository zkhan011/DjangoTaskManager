# coding: utf-8
# Copyright: Dmitriy Antonenko 2017

from django import forms
from django.forms import ModelForm
from .models import Task, Department, Project
from django.contrib.auth.models import User
from datetime import date
from .models import PRIORITY_TYPES
import calendar



class CreateTaskForm(ModelForm):
    """
    Create new task form
    """
    start_date = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                                     'placeholder': 'YYYY-MM-DD'},
                                                                              format='%Y-%m-%d'),
                                 input_formats=('%Y-%m-%d',), required=True)

    target_completion_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                           'placeholder': 'YYYY-MM-DD'},
                                                                    format='%Y-%m-%d'),
                                             input_formats=('%Y-%m-%d',), required=True)

    priority = forms.ChoiceField(choices=PRIORITY_TYPES,widget=forms.Select(attrs={'class': 'form-control input-sm'}))

    details = forms.CharField(required=True,
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control input-sm', 'rows': '2', 'placeholder': 'Task details'}))

    po = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',
                                                                       'placeholder': 'PO (if any)'}))

    assignee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=True)

    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=True)

    project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control input-sm',
                                                                'placeholder': 'Project (if any)'}),
                                     required=False)

    class Meta:
        model = Task
        exclude = ('number', 'owner', 'created', 'completed', 'completion_date', 'status', 'comments')


class AssigneeEditTaskForm(ModelForm):
    """
    Edit Comments and status form
    """
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '4',
                                                            'placeholder': 'Task details'}))

    status = forms.ChoiceField(choices=Task.STATUS_TYPE,
                               widget=forms.Select(attrs={'class': 'form-control input-sm'}))

    class Meta:
        model = Task
        fields = ('comments', 'status')
        #exclude = ('number', 'owner', 'created', 'completed', 'completion_date', 'start_date', 'target_completion_date',
        #           'details', 'po', 'assignee', 'department')


class OwnerEditTaskForm(CreateTaskForm):
    """
    Edit Task form. Owner can edit all fields
    """
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '2',
                                                            'placeholder': 'Task details'}))

    status = forms.ChoiceField(choices=Task.STATUS_TYPE,
                               widget=forms.Select(attrs={'class': 'form-control input-sm'}))

    completion_date = forms.DateField(initial=date.today(),
                                      widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                    'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
                                      input_formats=('%Y-%m-%d',), required=False)

    project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=False)

    class Meta:
        model = Task
        exclude = ('number', 'owner', 'created', )




class CreateProjectForm(ModelForm):
    """
    Create Project Form
    """
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control input-sm', }))

    pwo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',
                                                                        'placeholder': 'PWO (if any)'}))

    start_date = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                                     'placeholder': 'YYYY-MM-DD'},
                                                                              format='%Y-%m-%d'),
                                 input_formats=('%Y-%m-%d',), required=True)
    due_date = forms.DateField( widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                                   'placeholder': 'YYYY-MM-DD'},
                                                                            format='%Y-%m-%d'),
                               input_formats=('%Y-%m-%d',), required=True)

    department = forms.ModelChoiceField(queryset=Department.objects.all().exclude(name__exact='!Dummy'), #.order_by('name')
                                        widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=False)
    #owner = forms.ModelChoiceField(queryset=User.objects.all(),
    #                               widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=True)
    assignee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=True)

    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '2',
                                                            'placeholder': 'Project comments'}))

    class Meta:
        model = Project
        exclude = ('status', 'code', 'completed', 'created', 'owner')


class EditProjectForm(CreateProjectForm):

    owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=True)

    completed = forms.BooleanField(required=False)

    class Meta:
        model = Project
        #fields = ['name', 'pwo', 'start_date', 'due_date', 'department', 'assignee', 'owner', 'completed']
        exclude = ('status', 'code', 'created' )



class OwnerEditTaskFormAjax(CreateTaskForm):
    """
    Edit Task form. Owner can edit all fields
    """

    start_date = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                                     'placeholder': 'YYYY-MM-DD',
                                                                                     'data-validation': 'date',
                                                                                     'data-validation-format': 'yyyy-mm-dd',
                                                                                     },
                                                                              format='%Y-%m-%d'),
                                 input_formats=('%Y-%m-%d',), required=True)

    target_completion_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control input-sm',
                                                                           'placeholder': 'YYYY-MM-DD',
                                                                           'data-validation': 'date',
                                                                           'data-validation-format': 'yyyy-mm-dd',
                                                                           },
                                                                    format='%Y-%m-%d'),
                                             input_formats=('%Y-%m-%d',), required=True)

    details = forms.CharField(required=True,
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control input-sm',
                                         'rows': '2',
                                         'data-validation': 'required',
                                         'placeholder': 'Task details'}))

    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '2',
                                                            'placeholder': 'Task details'}))

    status = forms.ChoiceField(choices=Task.STATUS_TYPE,
                               widget=forms.Select(attrs={'class': 'form-control input-sm'}))

    # completion_date = forms.DateField(initial=date.today(),
    #                                   widget=forms.DateInput(attrs={'class': 'form-control input-sm',
    #                                                                 'placeholder': 'YYYY-MM-DD',
    #                                                                 'data-validation': 'date',
    #                                                                 'data-validation-format': 'yyyy-mm-dd',
    #                                                                 }, format='%Y-%m-%d'),
    #                                   input_formats=('%Y-%m-%d',), required=False)

    project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control input-sm'}), required=False)

    class Meta:
        model = Task
        exclude = ('number', 'owner', 'created', )


class TasksReport(forms.Form):
    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]  # [(1, 'January'), (2, 'February')]

    MONTHS.append((0, 'Current Month'))
    MONTHS.append((13, 'YTD'))

    #YEARS = [(year, year) for year in range(2020, 2011, -1)]
    period = forms.ChoiceField(choices=MONTHS, required=True, widget=forms.Select(attrs={'class': 'form-control input-sm'}))

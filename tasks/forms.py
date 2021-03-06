from django import forms
from django.forms import ModelForm
from django.forms import BaseModelFormSet

from django.core.validators import RegexValidator

from people.models import Staff
from .models import TaskCompletion


class TaskCompletionForm(ModelForm):
    """This form is to file completion of a task given an existing task"""
    class Meta:
        model = TaskCompletion
        # Only one field is on the form, the rest are passed in before
        fields = ['comment']

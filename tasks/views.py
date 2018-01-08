import os
import mimetypes

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib import messages

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from people.models import Staff

from .models import Task
from .models import TaskCompletion

from .forms import TaskCompletionForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group


@login_required()
def tasks_index(request):
    '''Obtains a list of all non archived tasks'''
    # Fetch the tasks assigned against the specific user of the staff member
    staff = get_object_or_404(Staff, user=request.user)
    tasks = staff.get_all_tasks()
    # tasks = Task.objects.all().exclude(archive=True).order_by('deadline')

    augmented_tasks = []
    for task in tasks:
        augmented_tasks.append([task, task.is_urgent(), task.is_overdue()])

    template = loader.get_template('tasks/index.html')
    context = {
        'augmented_tasks': augmented_tasks,
    }
    return HttpResponse(template.render(context, request))


@login_required()
def tasks_bystaff(request, staff_id):
    '''Show the tasks assigned against the specific user of the staff member'''
    staff = get_object_or_404(Staff, pk=staff_id)
    all_tasks = staff.get_all_tasks()

    # We will create separate lists for those tasks that are complete
    combined_list_complete = []
    combined_list_incomplete = []

    for task in all_tasks:
        # Is it complete? Look for a completion model
        completion = TaskCompletion.objects.all().filter(staff=staff).filter(task=task)
        if len(completion) == 0:
            combined_item = [task, task.is_urgent(), task.is_overdue()]
            combined_list_incomplete.append(combined_item)
        else:
            combined_item = [task, completion[0].when]
            combined_list_complete.append(combined_item)

    template = loader.get_template('tasks/bystaff.html')
    context = {
        'staff': staff,
        'combined_list_complete': combined_list_complete,
        'combined_list_incomplete': combined_list_incomplete,
    }
    return HttpResponse(template.render(context, request))


@login_required()
def tasks_details(request, task_id):
    '''Obtains a list of all completions for a given task'''
    # Get the task itself, and all targetted users
    task = get_object_or_404(Task, pk=task_id)
    all_targets = task.get_all_targets()

    combined_list_complete = []
    combined_list_incomplete = []

    for target in all_targets:
        # Is it complete? Look for a completion model
        completion = TaskCompletion.objects.all().filter(staff=target).filter(task=task)
        if len(completion) == 0:
            # Not complete, but only add the target if they aren't active
            if target.is_active():
                combined_item = [target, False]
                combined_list_incomplete.append(combined_item)
        else:
            combined_item = [target, completion[0]]
            combined_list_complete.append(combined_item)

    total_number = len(combined_list_complete) + len(combined_list_incomplete)
    if total_number > 0:
        percentage_complete = 100 * len(combined_list_complete) / total_number
    else:
        percentage_complete = 0

    template = loader.get_template('tasks/details.html')
    context = {
        'task': task,
        'overdue': task.is_overdue(),
        'urgent': task.is_urgent(),
        'combined_list_complete': combined_list_complete,
        'combined_list_incomplete': combined_list_incomplete,
        'percentage_complete': percentage_complete
    }
    return HttpResponse(template.render(context, request))


@login_required()
def tasks_completion(request, task_id, staff_id):
    """Processes recording of a task completion"""
    # Get the task itself, and all targetted users
    # TODO: check for existing completions
    # TODO: check staff is in *open* targets
    task = get_object_or_404(Task, pk=task_id)
    staff = get_object_or_404(Staff, pk=staff_id)
    all_targets = task.get_all_targets()

    # check the staff member is that currently logged in
    # or a user with permission to edit completions
    is_current_user = (request.user == staff.user)
    can_override = request.user.has_perm('loads.add_taskcompletion')
    if not (is_current_user or can_override):
        return HttpResponseRedirect(reverse('forbidden'))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskCompletionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.task = task
            new_item.staff = staff

            new_item.save()
            form.save_m2m()

            # redirect to the task details
            # TODO: which is a pain if we came from the bystaff view
            url = reverse('tasks_details', kwargs={'task_id': task_id})
            return HttpResponseRedirect(url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskCompletionForm()

    return render(request, 'tasks/completion.html', {'form': form, 'task': task,
            'overdue': task.is_overdue(),
            'urgent': task.is_urgent(), 'staff': staff})


"""Django Models for WAM project"""

import datetime

from django.db import models
from django.contrib.auth.models import User, Group

from core.models import Category
#from people.models import Staff


from django.core.validators import validate_comma_separated_integer_list

# code to handle timezones
from django.utils.timezone import utc

class Task(models.Model):
    """A task that members of staff will be allocated

    These are usually much smaller than Activities and are deadline driven

    name        a name for the task
    category    see the Category model
    details     a potentially large area of text giving more information
    deadline    the time by which the task should be completed
    archive     whether the task is completed / archived
    targets     those staff the task is allocated to

    See also the TaskCompletion model. Note that targets should not be removed
    on completion.
    """

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    details = models.TextField()
    deadline = models.DateTimeField()
    archive = models.BooleanField(default=False)
    targets = models.ManyToManyField('people.Staff', blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' due ' + str(self.deadline)

    def get_all_targets(self):
        """obtains all targets for a task whether by user or group, returns a list of valid targets"""
        # These are staff objects
        target_by_users = self.targets.all().order_by('user__last_name')
        target_groups = self.groups.all()
        # These are user objects
        target_by_groups = User.objects.all().filter(groups__in=target_groups).distinct().order_by('last_name')

        # Start to build a queryset, starting with targetted users
        all_targets = target_by_users

        # Add each collection of staff members implicated by group
        for user in target_by_groups:
            staff = Staff.objects.all().filter(user=user)
            all_targets = all_targets | staff

        # Use distinct to clean up any duplicates
        all_targets = all_targets.distinct()

        return all_targets

    def is_urgent(self):
        """returns True is the task is 7 days away or less, False otherwise"""
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        seconds_left = (self.deadline - now).total_seconds()
        # If a task is less than a week from deadline consider it urgent
        return bool(seconds_left < 60 * 60 * 24 * 7)

    def is_overdue(self):
        """returns True is the deadline has passed, False otherwise"""
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        seconds_left = (self.deadline - now).total_seconds()
        return bool(seconds_left < 0)


class TaskCompletion(models.Model):
    """This indicates that a staff member has completed a given task

    task    See the Task model
    Staff   See the Staff model
    when    a datetime stamp of when the task was completed
    comment an optional comment on completion

    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    staff = models.ForeignKey('people.Staff', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, default='', blank=True)
    when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task.name + ' completed by ' + str(self.staff) + ' on ' + str(self.when)





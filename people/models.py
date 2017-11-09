# We are building on standard Django User and Group

from django.contrib.auth.models import User, Group

from django.db import models

from tasks.models import Task


# Create your models here.
class StaffManager(models.Manager):
    """Manager for staff to enforce ordering

    The Staff object is linked to the User object, but there seems no way to enforce
    default ordering by User.last_name short of this."""

    # TODO: This may not be necessary in the future if a custom admin interface is put in place

    def get_queryset(self):
        return super(StaffManager, self).get_queryset().order_by("user__last_name", "user__first_name")


class Staff(models.Model):
    """Augments the Django user model with staff details

    user            the Django user object, a one to one link
    title           the title of the member of staff (Dr, Mr etc)
    staff_number    the staff number
    fte             the percentage of time the member of staff is available for
    package         the active work package to edit or display
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    staff_number = models.CharField(max_length=20)

    objects = StaffManager()

    def __str__(self):
        return self.title + ' ' + self.user.first_name + ' ' + self.user.last_name

    def first_name(self):
        """return the first name of the linked user account"""
        return self.user.first_name

    def last_name(self):
        """return the last name of the linked user account"""
        return self.user.last_name

    def is_active(self):
        """Maps to whether the underlying user is active"""
        return self.user.is_active

    def get_all_tasks(self):
        """Returns a queryset of all unarchived tasks linked to this staff member"""
        user_tasks = Task.objects.all().filter(targets=self).exclude(archive=True).distinct().order_by('deadline')

        # And those assigned against the group
        groups = Group.objects.all().filter(user=self.user)
        group_tasks = Task.objects.all().filter(groups__in=groups).exclude(archive=True).distinct().order_by('deadline')

        # Combine them
        all_tasks = user_tasks | group_tasks

        return all_tasks

    class Meta:
        verbose_name_plural = 'staff'

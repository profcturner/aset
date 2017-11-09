from django.contrib import admin

from .models import Task
from .models import TaskCompletion


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'deadline')
    list_filter = ('archive', 'category')


class TaskCompletionAdmin(admin.ModelAdmin):
    list_display = ('task', 'staff', 'when', 'comment')


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCompletion, TaskCompletionAdmin)

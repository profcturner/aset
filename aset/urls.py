"""aset URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.contrib.auth import views as auth_views


# Load views from multiple apps and clarify which are which
from core import views as core_views
from tasks import views as task_views

urlpatterns = [
    url(r'^$', core_views.index, name="index"),
    url(r'^accounts/login/$', auth_views.LoginView.as_view()),
    url(r'^tasks/index/$', task_views.tasks_index, name='tasks_index'),
    url(r'^tasks/completion/(?P<task_id>[0-9]+)/(?P<staff_id>[0-9]+)$', task_views.tasks_completion,
        name='tasks_completion'),
    url(r'^tasks/detail/(?P<task_id>[0-9]+)$', task_views.tasks_details, name='tasks_details'),
    url(r'^tasks/bystaff/(?P<staff_id>[0-9]+)$', task_views.tasks_bystaff, name='tasks_bystaff'),
    url(r'^admin/', admin.site.urls),

]

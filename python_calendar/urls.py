"""python_calendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from calendar_events.models import index
from calendar_events.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("statistics", statistics, name="statistics"),

    #Events views
    path("api/events/", getEvents, name="events"),
    path("api/events/<str:pk>/update", updateEvent, name="update_event"),
    path("api/events/<str:pk>/delete", deleteEvent, name="delete_event"),
    path("api/events/<str:pk>", getEvent, name="event"),
    path("api/events/<str:user_id>/<str:cat_id>/<str:name>/<str:repeat_id>/<str:first_occ>/<str:desc>/<str:dur>/<str:prio_id>/<str:rem_time>/<str:loc>/<str:color>/add",
        addEvent, name="add_event"),

    #Event categories views
    path("api/event_categories/", getEventCategories, name="event_categories"),
    path("api/event_categories/<str:user_id>/<str:name>/<str:prio_id>/<str:dur>/<str:desc>/<str:loc>/<str:color>/<str:rem_time>/add",
         addEventCategory, name="add_event_category"),


    #Event occurrences views
    path("api/event_occurrences/", getEventOccurrences, name="event_occurrences"),
    path("api/event_occurrences/<str:start_time>/<str:end_time>/get_occurrences_interval", getEventOccurrencesFromInterval, name="event_occurrences_interval"),

    #Tasks views
    path("api/tasks/", getTasks, name="tasks"),
    path("api/tasks/<str:pk>", getTasks, name="task"),
    path("api/tasks/<str:user_id>/<str:cat_id>/<str:prio_id>/<str:repeat_id>/<str:name>/<str:exp_completion_date>/<str:first_occ>/<str:desc>/<str:rem_time>/<str:loc>/<str:color>/<str:deadline>/<str:slide>/<str:parent_id>/add",
        addTask, name="add_task"),

    #Task categories views
    path("api/task_categories/", getTaskCategories, name="task_categories"),
    path("api/task_categories/<str:user_id>/<str:name>/<str:prio_id>/<str:slide>/<str:desc>/<str:rem_time>/<str:loc>/<str:color>/<str:deadline>/add",
         addTaskCategory, name="add_task_category"),

    #Task occurrences views
    path("api/task_occurrences/", getTaskOccurrences, name="task_occurrences"),
    path("api/task_occurrences/<str:start_time>/<str:end_time>/get_occurrences_interval", getTaskOccurrencesFromInterval, name="task_occurrences_interval"),

    #Notes views
    path("api/notes/", getNotes, name="notes"),
    path("api/notes/<str:pk>", getNote, name="note"),
    path("api/notes/<str:user_id>/<str:title>/<str:content>/<str:prio_id>/add", addNote, name="add_note"),

    #Priority level views
    path("api/priority_levels/", getPriorityLevels, name="priority_levels"),
    path("api/priority_levels/<str:pk>", getPriorityLevel, name="priority_level"),
    path("api/priority_levels/<str:user_id>/<str:name>/<str:priority>/<str:rem_time>/<str:markdown>/add", addPriorityLevel, name="add_priority_level"),

    #Repeat patterns views
    path("api/repeat_patterns/", getRepeatPatterns, name="repeat_patterns"),
    path("api/repeat_patterns/<std:pk>", getRepeatPattern, name="repeat_pattern"),
    path("api/repeat_patterns/<str:user_id>/<str:name>/<str:days>/<str:weeks>/<str:months>/<str:years>/<str:repeats>/add", addRepeatPattern, name="add_repeat_pattern"),

    #Users views
    path("api/users/", getUsers, name="users"),
    path("api/users/<std:pk>", getUser, name="user"),
    path("api/users/<str:login>/add", addUser, name="add_user"),
]

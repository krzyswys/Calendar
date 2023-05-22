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
    path("api/events/", getEvents, name="events"),
    path("api/events/<str:pk>/update", updateEvent, name="update_event"),
    path("api/events/<str:pk>/delete", deleteEvent, name="delete_event"),
    path("api/events/<str:pk>", getEvent, name="event"),
    path("api/event_categories/", getEventCategories, name="event_categories"),
    path("api/event_occurrences/", getEventOccurrences, name="event_occurrences"),
    path("api/event_occurrences/<str:start_time>/<str:end_time>/get_occurrences_interval", getEventOccurrencesFromInterval, name="event_occurrences_interval"),
    path("api/tasks/", getTasks, name="tasks"),
    path("api/tasks/<str:pk>", getTasks, name="task"),
    path("api/task_categories/", getTaskCategories, name="task_categories"),
    path("api/task_occurrences/", getTaskOccurrences, name="task_occurrences"),
    path("api/task_occurrences/<str:start_time>/<str:end_time>/get_occurrences_interval", getTaskOccurrencesFromInterval, name="task_occurrences_interval"),
    path("api/notes/", getNotes, name="notes"),
    path("api/notes/<str:pk>", getNote, name="note"),
    path("api/priority_levels/", getPriorityLevels, name="priority_levels"),
    path("api/priority_levels/<str:pk>", getPriorityLevel, name="priority_level"),
    path("api/repeat_patterns/", getRepeatPatterns, name="repeat_patterns"),
    path("api/repeat_patterns/<std:pk>", getRepeatPattern, name="repeat_pattern"),
    path("api/users/", getUsers, name="users"),
    path("api/users/<std:pk>", getUser, name="user"),
]

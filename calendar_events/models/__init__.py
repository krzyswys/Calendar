from calendar_events.models.users import Users
from calendar_events.models.eventCategories import EventCategories
from calendar_events.models.priorityLevels import PriorityLevels
from calendar_events.models.repeatPattern import RepeatPatterns
from calendar_events.models.events import Events
from calendar_events.models.events import EventOccurrences
from calendar_events.models.taskCategories import TaskCategories
from calendar_events.models.tasks import Tasks
from calendar_events.models.tasks import TaskOccurrences
from calendar_events.models.notes import Notes

from django.shortcuts import render


def index(request):
    users = Users.objects.all()
    priority_levels = PriorityLevels.objects.all()
    event_categories = EventCategories.objects.all()
    repeat_patterns = RepeatPatterns.objects.all()
    events = Events.objects.all()
    task_categories = TaskCategories.objects.all()
    tasks = Tasks.objects.all()
    notes = Notes.objects.all()
    event_occurences = EventOccurrences.objects.all()
    tasks_occurences = TaskOccurrences.objects.all()
    context = {
        "users": users,
        "priority_levels": priority_levels,
        "event_categories": event_categories,
        "repeat_patterns": repeat_patterns,
        "events": events,
        "task_categories": task_categories,
        "tasks": tasks,
        "notes": notes,
        "event_occurences": event_occurences,
        "tasks_occurences": tasks_occurences,
    }

    return render(request, "index.html", context)

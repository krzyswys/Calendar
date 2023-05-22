from django.shortcuts import render
from .events_statistic import *
from .tasks_statistic import *


def tasks_efficiency():
    tasks = Tasks.objects.all()
    efficiency_dict = {}
    for task in tasks:
        ans = {"name": task.name, "efficiency": calculate_efficiency_of_task(task)}
        efficiency_dict[task.task_id] = ans
    return efficiency_dict


def tasks_efficiency_priority():
    tasks = Tasks.objects.all()
    efficiency_dict = {}
    for task in tasks:
        ans = {
            "name": task.name,
            "efficiency": calculate_efficiency_with_priority_of_task(task),
        }
        efficiency_dict[task.task_id] = ans
    return efficiency_dict


def statistics(request):
    # Events:
    categories_duration = calculate_event_duration_by_category()
    priority_duration = calculate_event_duration_by_priority()
    location_stats = calculate_location_stats()
    priority_stats = calculate_priority_stats()
    # Tasks:
    percentage_tasks_deadline_completed = percentage_tasks_completed_by_priority(
        deadline=True
    )
    percentage_tasks_completed_slidetime = percentage_tasks_completed_by_priority(
        deadline=False, slidetime=True
    )
    percentage_tasks_completed_expectedtime = percentage_tasks_completed_by_priority(
        deadline=False, slidetime=False, expectedtime=True
    )
    calculate_deadline_completion_percentage_category_till_now = (
        calculate_completion_percentage_by_category_till_now(deadline=True)
    )
    calculate_slidetime_completion_percentage_category_till_now = (
        calculate_completion_percentage_by_category_till_now(
            deadline=False, slidetime=True
        )
    )
    calculate_expectedtime_completion_percentage_category_till_now = (
        calculate_completion_percentage_by_category_till_now(
            deadline=False, slidetime=False, expectedtime=True
        )
    )
    calculate_average_completion_time_category_deadline = (
        calculate_average_completion_time_by_category(deadline=True)
    )
    calculate_average_completion_time_category_slidetime = (
        calculate_average_completion_time_by_category(deadline=False, slidetime=True)
    )
    calculate_average_completion_time_category_expectedtime = (
        calculate_average_completion_time_by_category(
            deadline=False, slidetime=False, expectedtime=True
        )
    )
    calculate_average_completion_time_priority_deadline = (
        calculate_average_completion_time_by_priority(deadline=True)
    )
    calculate_average_completion_time_prioritiy_slidetime = (
        calculate_average_completion_time_by_priority(deadline=False, slidetime=True)
    )
    calculate_average_completion_time_priority_expectedtime = (
        calculate_average_completion_time_by_priority(
            deadline=False, slidetime=False, expectedtime=True
        )
    )
    calculate_task_time_category = calculate_task_time_by_category()
    calculate_task_time_priority = calculate_task_time_by_priority()
    tasks_efficiencies = tasks_efficiency()
    tasks_efficiencies_priority = tasks_efficiency_priority()
    context = {
        "categories_duration": categories_duration,
        "priority_duration": priority_duration,
        "location_stats": location_stats,
        "priority_stats": priority_stats,
        "percentage_tasks_deadline_completed": percentage_tasks_deadline_completed,
        "percentage_tasks_completed_slidetime": percentage_tasks_completed_slidetime,
        "percentage_tasks_completed_expectedtime": percentage_tasks_completed_expectedtime,
        "calculate_deadline_completion_percentage_category_till_now": calculate_deadline_completion_percentage_category_till_now,
        "calculate_slidetime_completion_percentage_category_till_now": calculate_slidetime_completion_percentage_category_till_now,
        "calculate_expectedtime_completion_percentage_category_till_now": calculate_expectedtime_completion_percentage_category_till_now,
        "calculate_average_completion_time_category_deadline": calculate_average_completion_time_category_deadline,
        "calculate_average_completion_time_category_slidetime": calculate_average_completion_time_category_slidetime,
        "calculate_average_completion_time_category_expectedtime": calculate_average_completion_time_category_expectedtime,
        "calculate_average_completion_time_priority_deadline": calculate_average_completion_time_priority_deadline,
        "calculate_average_completion_time_prioritiy_slidetime": calculate_average_completion_time_prioritiy_slidetime,
        "calculate_average_completion_time_priority_expectedtime": calculate_average_completion_time_priority_expectedtime,
        "calculate_task_time_category": calculate_task_time_category,
        "calculate_task_time_priority": calculate_task_time_priority,
        "tasks_efficiencies": tasks_efficiencies,
        "tasks_efficiencies_priority": tasks_efficiencies_priority,
    }
    return render(request, "statistics.html", context)


from rest_framework.decorators import api_view
from .models.events import *
from rest_framework.response import Response
from .serializer import *
from django.shortcuts import render

# Events views

@api_view(["GET"])
def getEvents(request):
    events = Events.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getEvent(request, pk):
    event = Events.objects.filter(event_id=pk).first()
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(["PUT"])
def updateEvent(request, pk):
    data = request.data
    event = Events.objects.filter(event_id=pk).first()
    event.modify(
        description=data["description"],
    )
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(["DELETE"])
def deleteEvent(request, pk):
    event = Events.objects.filter(event_id=pk).first()
    event.delete()
    return Response("Event deleted")


@api_view(["GET"])
def getEventCategories(request):
    categories = EventCategories.objects.all()
    serializer = EventCategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getEventOccurrences(request):
    occurrences = EventOccurrences.objects.all()
    serializer = EventOccurrencesSerializer(occurrences, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getEventOccurrencesFromInterval(request, start_time, end_time):
    # Pattern: day-month-year
    start_day, start_month, start_year = start_time.split('-')
    end_day, end_month, end_year = end_time.split('-')

    start_time = datetime(int(start_year), int(start_month), int(start_day))
    end_time = datetime(int(end_year), int(end_month), int(end_day))

    occurrences = EventOccurrences.get_event_occurrences(time_start=start_time, time_stop=end_time)
    serializer = EventOccurrencesSerializer(occurrences, many=True)
    return Response(serializer.data)


# Tasks views

@api_view(["GET"])
def getTasks(request):
    tasks = Tasks.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getTask(request, pk):
    task = Tasks.objects.filter(event_id=pk).first()
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(["GET"])
def getTaskCategories(request):
    categories = TaskCategories.objects.all()
    serializer = TaskCategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getTaskOccurrences(request):
    occurrences = TaskOccurrences.objects.all()
    serializer = TaskOccurrencesSerializer(occurrences, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getTaskOccurrencesFromInterval(request, start_time, end_time):
    start_day, start_month, start_year = start_time.split('-')
    end_day, end_month, end_year = end_time.split('-')

    start_time = datetime(int(start_year), int(start_month), int(start_day))
    end_time = datetime(int(end_year), int(end_month), int(end_day))

    occurrences = TaskOccurrences.get_task_occurrences(time_start=start_time, time_stop=end_time)
    serializer = TaskOccurrencesSerializer(occurrences, many=True)
    return Response(serializer.data)


# Notes views


@api_view(["GET"])
def getNotes(request):
    notes = Notes.objects.all()
    serializer = NotesSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getNote(request, pk):
    note = Notes.objects.filter(note_id=pk).first()
    serializer = NotesSerializer(note, many=False)
    return Response(serializer.data)


# Priority levels views


@api_view(["GET"])
def getPriorityLevels(request):
    levels = PriorityLevels.objects.all()
    serializer = PriorityLevelsSerializer(levels, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getPriorityLevel(request, pk):
    level = PriorityLevels.objects.filter(priority_level_id=pk).first()
    serializer = PriorityLevelsSerializer(level, many=False)
    return Response(serializer.data)

# Repeat patterns views


@api_view(["GET"])
def getRepeatPatterns(request):
    patterns = RepeatPatterns.objects.all()
    serializer = RepeatPatternsSerializer(patterns, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getRepeatPattern(request, pk):
    pattern = RepeatPatterns.objects.filter(repeat_pattern_id=pk)
    serializer = RepeatPatternsSerializer(pattern, many=False)
    return Response(serializer.data)


# Users views


@api_view(["GET"])
def getUsers(request):
    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getUser(request, pk):
    user = Users.objects.filter(user_id=pk).first()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
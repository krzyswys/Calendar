from django.shortcuts import render
from .events_statistic import *
from .tasks_statistic import *
import exceptions as e


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


@api_view(["PUT"])
def addEvent(request):
    data = request.data

    #First occurrence pattern: day-month-year
    if data['first_occ'] != 'None':
        day, month, year = data['first_occ'].split('-')
        time = datetime(int(year), int(month), int(day))
    else:
        time = None

    #Duration pattern: seconds-minutes-hours-days
    if data['dur'] != 'None':
        seconds, minutes, hours, days = data['dur'].split('-')
        duration = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        duration = None

    #Reminder time pattern: seconds-minutes-hours-days
    if data['rem_time'] != 'None':
        seconds, minutes, hours, days = data['rem_time'].split('-')
        reminder_time = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        reminder_time = None

    event = None

    try:
        event = Events.create_event(
            Users.get_user(int(data['user_id'])),
            EventCategories.get_event_category(int(data['cat_id'])),
            data['name'],
            RepeatPatterns.get_repeat_pattern(int(data['repeat_id'])),
            time,
            data['desc'] if data['desc'] != 'None' else None,
            duration,
            PriorityLevels.get_priority_levels(int(data['prio_id'])) if data['prio_id'] != 'None' else None,
            reminder_time,
            data['loc'] if data['loc'] != 'None' else None,
            data['color'] if data['color'] != 'None' else None
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create an event')

    serializer = EventSerializer(event)
    return Response(serializer.data)


# Event categories views

@api_view(["GET"])
def getEventCategories(request):
    categories = EventCategories.objects.all()
    serializer = EventCategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
def addEventCategory(request):
    data = request.data

    # Duration pattern: seconds-minutes-hours-days
    if data['dur'] != 'None':
        seconds, minutes, hours, days = data['dur'].split('-')
        duration = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        duration = None

    # Reminder time pattern: seconds-minutes-hours-days
    if data['rem_time'] != 'None':
        seconds, minutes, hours, days = data['rem_time'].split('-')
        reminder_time = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        reminder_time = None

    event_category = None

    try:
        event_category = EventCategories.create_event_category(
            Users.get_user(int(data['user_id'])),
            data['name'],
            PriorityLevels.get_priority_levels(int(data['prio_id'])),
            duration,
            data['desc'] if data['desc'] != 'None' else None,
            data['loc'] if data['loc'] != 'None' else None,
            data['color'] if data['color'] != 'None' else None,
            reminder_time
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create an event category')

    serializer = EventCategoriesSerializer(event_category)
    return Response(serializer.data)


# Event occurrences views

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


@api_view(["PUT"])
def addTask(request):
    data = request.data

    # Expected completion date pattern: day-month-year
    if data['exp_completion_date'] != 'None':
        day, month, year = data['exp_completion_date'].split('-')
        expected_completion_date = datetime(int(year), int(month), int(day))
    else:
        expected_completion_date = None

    # First occurrence pattern: day-month-year
    if data['first_occ'] != 'None':
        day, month, year = data['first_occ'].split('-')
        first_occurrence = datetime(int(year), int(month), int(day))
    else:
        first_occurrence = None

    # Reminder time pattern: seconds-minutes-hours-days
    if data['rem_time'] != 'None':
        seconds, minutes, hours, days = data['rem_time'].split('-')
        reminder_time = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        reminder_time = None

    # Deadline: day-month-year
    if data['deadline'] != 'None':
        day, month, year = data['deadline'].split('-')
        deadline = datetime(int(year), int(month), int(day))
    else:
        deadline = None

    # Slide time: seconds-minutes-hours-days
    if data['slide'] != 'None':
        seconds, minutes, hours, days = data['slide'].split('-')
        slide = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        slide = None

    task = None

    try:
        task = Tasks.create_task(
            Users.get_user(int(data['user_id'])),
            TaskCategories.get_task_categories(int(data['cat_id'])),
            PriorityLevels.get_priority_levels(int(data['prio_id'])),
            RepeatPatterns.get_repeat_pattern(int(data['repeat_id'])),
            data['name'],
            expected_completion_date,
            first_occurrence,
            data['desc'] if data['desc'] != 'None' else None,
            reminder_time,
            data['loc'] if data['loc'] != 'None' else None,
            data['color'] if data['color'] != 'None' else None,
            deadline,
            slide,
            Users.get_user(int(data['parent_id'])) if data['parent_id'] != 'None' else None
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create a task')

    serializer = TaskSerializer(task)
    return Response(serializer.data)


# Task categories views

@api_view(["GET"])
def getTaskCategories(request):
    categories = TaskCategories.objects.all()
    serializer = TaskCategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
def addTaskCategory(request):
    data = request.data

    # Slide time: seconds-minutes-hours-days
    if data['slide'] != 'None':
        seconds, minutes, hours, days = data['slide'].split('-')
        slide = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        slide = None

    # Reminder time pattern: seconds-minutes-hours-days
    if data['rem_time'] != 'None':
        seconds, minutes, hours, days = data['rem_time'].split('-')
        reminder_time = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        reminder_time = None

    # Deadline: seconds-minutes-hours-days
    if data['deadline'] != 'None':
        seconds, minutes, hours, days = data['deadline'].split('-')
        deadline = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        deadline = None

    task_category = None

    try:
        task_category = TaskCategories.create_task_category(
            Users.get_user(int(data['user_id'])),
            data['name'],
            PriorityLevels.get_priority_levels(int(data['prio_id'])),
            slide,
            data['desc'] if data['desc'] != 'None' else None,
            reminder_time,
            data['loc'] if data['loc'] != 'None' else None,
            data['color'] if data['color'] != 'None' else None,
            deadline
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create a task category')

    serializer = TaskCategoriesSerializer(task_category)
    return Response(serializer.data)


# Task occurrences views

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


@api_view(["PUT"])
def addNote(request):
    data = request.data

    note = None

    try:
        note = Notes.create_note(
            Users.get_user(int(data['user_id'])),
            data['title'],
            data['content'] if data['content'] != 'None' else None,
            PriorityLevels.get_priority_levels(int(data['prio_id'])) if data['prio_id'] != 'None' else None
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create a note')

    serializer = NotesSerializer(note)
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


@api_view(["PUT"])
def addPriorityLevel(request):
    data = request.data

    # Reminder time pattern: seconds-minutes-hours-days
    if data['rem_time'] != 'None':
        seconds, minutes, hours, days = data['rem_time'].split('-')
        reminder_time = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    else:
        reminder_time = None

    priority_level = None

    try:
        priority_level = PriorityLevels.create_priority_level(
            Users.get_user(int(data['user_id'])),
            data['name'],
            int(data['priority']),
            reminder_time,
            data['markdown'] if data['markdown'] != 'None' else None
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create a priority level')

    serializer = PriorityLevelsSerializer(priority_level)
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


@api_view(["PUT"])
def addRepeatPattern(request):
    data = request.data

    repeat_pattern = None

    try:
        repeat_pattern = RepeatPatterns.create_repeat_pattern(
            Users.get_user(int(data['user_id'])),
            data['name'],
            int(data['days']),
            int(data['weeks']),
            int(data['months']),
            int(data['years']),
            int(data['repeats'])
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create a repeat pattern')

    serializer = RepeatPatternsSerializer(repeat_pattern)
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


@api_view(["PUT"])
def addUser(request):
    data = request.data

    user = None

    try:
        user = Users.create_user(
            data['login']
        )
    except e.EntityAlreadyExists | e.ObjectDoesNotExist:
        return Response('Cannot create an user')

    serializer = UserSerializer(user)
    return Response(serializer.data)
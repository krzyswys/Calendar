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

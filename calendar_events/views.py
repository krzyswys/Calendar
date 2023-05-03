from django.shortcuts import render
from .events_statistic import *
from .tasks_statistic import *


# FIXME: calculate_deadline_completion_percentage_category_till_now make it accept time period
# TODO: make all request accept time period
def event_statistics(request):
    categories_duration = calculate_event_duration_by_category()
    priority_duration = calculate_event_duration_by_priority()
    location_stats = calculate_location_stats()
    priority_stats = calculate_priority_stats()
    #
    percentage_tasks_deadline_completed = percentage_tasks_completed_by_priority()
    percentage_tasks_completed_slidetime = percentage_tasks_completed_by_slidetime()
    percentage_tasks_completed_expectedtime = (
        percentage_tasks_completed_by_expectedtime()
    )
    calculate_deadline_completion_percentage_category_till_now = (
        calculate_deadline_completion_percentage_by_category_till_now()
    )
    calculate_slidetime_completion_percentage_category_till_now = (
        calculate_slidetime_completion_percentage_by_category_till_now()
    )
    calculate_expectedtime_completion_percentage_category_till_now = (
        calculate_expectedtime_completion_percentage_by_category_till_now()
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
    }
    return render(request, "event_statistics.html", context)

from django.shortcuts import render
from .models import Events
from .events_statistic import *


def event_statistics(request):
    categories_duration = calculate_event_duration_by_category()
    return render(
        request, "event_statistics.html", {"categories_duration": categories_duration}
    )

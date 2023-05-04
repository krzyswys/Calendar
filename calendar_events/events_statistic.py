from calendar_events.models import Events, EventCategories
from django.db.models import Sum, Count


def calculate_event_duration_by_category(start_date=None, end_date=None):
    result = {}
    categories = (
        Events.objects.order_by().values_list("event_category", flat=True).distinct()
    )
    event_categories = EventCategories.objects.filter(event_category_id__in=categories)
    events = Events.objects.all()
    if start_date:
        events = events.filter(start_time__gte=start_date)
    if end_date:
        events = events.filter(end_time__lte=end_date)
    for category in event_categories:
        duration_sum = events.filter(event_category=category).aggregate(
            duration_sum=Sum("duration")
        )["duration_sum"]
        result[category.name] = duration_sum

    return result


def calculate_event_duration_by_priority(start_date=None, end_date=None):
    result = {}
    priorities = (
        Events.objects.order_by()
        .values_list("priority_level__priority_value", flat=True)
        .distinct()
    )
    events = Events.objects.all()
    if start_date:
        events = events.filter(start_time__gte=start_date)
    if end_date:
        events = events.filter(end_time__lte=end_date)
    for priority in priorities:
        duration_sum = events.filter(priority_level__priority_value=priority).aggregate(
            duration_sum=Sum("duration")
        )["duration_sum"]
        result[priority] = duration_sum

    return result


def calculate_location_stats(start_date=None, end_date=None):
    events = Events.objects.all()
    if start_date:
        events = events.filter(start_time__gte=start_date)
    if end_date:
        events = events.filter(end_time__lte=end_date)
    total_events = events.count()
    location_stats = (
        events.values("localization")
        .annotate(count=Count("localization"))
        .order_by("-count")
    )

    return {
        loc["localization"]: round((loc["count"] / total_events) * 100, 2)
        for loc in location_stats
    }


def calculate_priority_stats(start_date=None, end_date=None):
    events = Events.objects.all()
    if start_date:
        events = events.filter(start_time__gte=start_date)
    if end_date:
        events = events.filter(end_time__lte=end_date)
    total_events = events.count()
    priority_stats = (
        events.values("priority_level__priority_value")
        .annotate(count=Count("priority_level__priority_value"))
        .order_by("-priority_level__priority_value")
    )

    return {
        p["priority_level__priority_value"]: round((p["count"] / total_events) * 100, 2)
        for p in priority_stats
    }

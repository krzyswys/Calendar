from calendar_events.models import Events, EventCategories
from django.db.models import Sum, Count


def calculate_event_duration_by_category():
    result = {}
    categories = (
        Events.objects.order_by().values_list("event_category", flat=True).distinct()
    )
    event_categories = EventCategories.objects.filter(event_category_id__in=categories)
    for category in event_categories:
        duration_sum = Events.objects.filter(event_category=category).aggregate(
            duration_sum=Sum("duration")
        )["duration_sum"]
        result[category.name] = duration_sum

    return result


def calculate_event_duration_by_priority():
    result = {}
    priorities = (
        Events.objects.order_by()
        .values_list("priority_level__priority_value", flat=True)
        .distinct()
    )
    for priority in priorities:
        duration_sum = Events.objects.filter(
            priority_level__priority_value=priority
        ).aggregate(duration_sum=Sum("duration"))["duration_sum"]
        result[priority] = duration_sum

    return result


def calculate_location_stats():
    total_events = Events.objects.count()
    location_stats = (
        Events.objects.values("localization")
        .annotate(count=Count("localization"))
        .order_by("-count")
    )

    return {
        loc["localization"]: round((loc["count"] / total_events) * 100, 2)
        for loc in location_stats
    }


def calculate_priority_stats():
    total_events = Events.objects.count()
    priority_stats = (
        Events.objects.values("priority_level__priority_value")
        .annotate(count=Count("priority_level__priority_value"))
        .order_by("-priority_level__priority_value")
    )

    return {
        p["priority_level__priority_value"]: round((p["count"] / total_events) * 100, 2)
        for p in priority_stats
    }

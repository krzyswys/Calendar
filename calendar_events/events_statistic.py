from calendar_events.models import Events, EventCategories
from django.db.models import Sum, Count


def calculate_event_duration_by_category():
    result = {}
    categories = (
        Events.objects.order_by().values_list("EventCategory", flat=True).distinct()
    )
    event_categories = EventCategories.objects.filter(event_category_id__in=categories)
    for category in event_categories:
        duration_sum = Events.objects.filter(EventCategory=category).aggregate(
            duration_sum=Sum("Duration")
        )["duration_sum"]
        result[category.name] = duration_sum

    return result


def calculate_event_duration_by_priority():
    result = {}
    priorities = (
        Events.objects.order_by()
        .values_list("PriorityLevel__priority_value", flat=True)
        .distinct()
    )
    for priority in priorities:
        duration_sum = Events.objects.filter(
            PriorityLevel__priority_value=priority
        ).aggregate(duration_sum=Sum("Duration"))["duration_sum"]
        result[priority] = duration_sum

    return result


def calculate_location_stats():
    total_events = Events.objects.count()
    location_stats = (
        Events.objects.values("Localization")
        .annotate(count=Count("Localization"))
        .order_by("-count")
    )

    return {
        loc["Localization"]: round((loc["count"] / total_events) * 100, 2)
        for loc in location_stats
    }


def calculate_priority_stats():
    total_events = Events.objects.count()
    priority_stats = (
        Events.objects.values("PriorityLevel__priority_value")
        .annotate(count=Count("PriorityLevel__priority_value"))
        .order_by("-PriorityLevel__priority_value")
    )

    return {
        p["PriorityLevel__priority_value"]: round((p["count"] / total_events) * 100, 2)
        for p in priority_stats
    }

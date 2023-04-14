from calendar_events.models import Tasks, PriorityLevels, TaskCategories
from django.db.models import Sum, F, Avg, Count, Q, FloatField, When, Case
from django.utils import timezone

# FIXME: only one handler for calculate_average_completion_time_by_priority & calculate_average_completion_time_by_category


def calculate_efficiency(task: Tasks):
    if task.completion_date is None:
        return None

    time_diff = task.completion_date - task.creation_date
    expected_time_diff = task.expected_completion_date - task.creation_date
    deadline_diff = task.deadline - task.creation_date

    if task.deadline < task.expected_completion_date:
        if task.completion_date <= task.deadline:
            if task.completion_date <= task.expected_completion_date:
                efficiency = round(
                    (expected_time_diff.total_seconds() / time_diff.total_seconds())
                    * 100,
                    2,
                )
            else:
                slide_time_diff = task.completion_date - task.expected_completion_date
                slide_time_allowed = (
                    task.deadline
                    + task.acceptable_slide_time
                    - task.expected_completion_date
                )
                efficiency = round(
                    (
                        (
                            slide_time_allowed.total_seconds()
                            - slide_time_diff.total_seconds()
                        )
                        / slide_time_allowed.total_seconds()
                    )
                    * 100,
                    2,
                )
        else:
            efficiency = round(
                (deadline_diff.total_seconds() / time_diff.total_seconds()) * 100, 2
            )
    else:
        if task.completion_date <= task.expected_completion_date:
            efficiency = round(
                (expected_time_diff.total_seconds() / time_diff.total_seconds()) * 100,
                2,
            )
        else:
            efficiency = round(
                (deadline_diff.total_seconds() / time_diff.total_seconds()) * 100, 2
            )

    return efficiency


def calculate_efficiency_with_priority(task):
    if task.completion_date is None:
        return None

    time_diff = task.completion_date - task.creation_date
    expected_time_diff = task.expected_completion_date - task.creation_date
    deadline_diff = task.deadline - task.creation_date

    if task.deadline < task.expected_completion_date:
        if task.completion_date <= task.deadline:
            if task.completion_date <= task.expected_completion_date:
                efficiency = round(
                    (expected_time_diff.total_seconds() / time_diff.total_seconds())
                    * 100,
                    2,
                )
            else:
                slide_time_diff = task.completion_date - task.expected_completion_date
                slide_time_allowed = (
                    task.deadline
                    + task.acceptable_slide_time
                    - task.expected_completion_date
                )
                efficiency = round(
                    (
                        (
                            slide_time_allowed.total_seconds()
                            - slide_time_diff.total_seconds()
                        )
                        / slide_time_allowed.total_seconds()
                    )
                    * 100,
                    2,
                )
        else:
            efficiency = round(
                (deadline_diff.total_seconds() / time_diff.total_seconds()) * 100, 2
            )
    else:
        if task.completion_date <= task.expected_completion_date:
            efficiency = round(
                (expected_time_diff.total_seconds() / time_diff.total_seconds()) * 100,
                2,
            )
        else:
            efficiency = round(
                (deadline_diff.total_seconds() / time_diff.total_seconds()) * 100, 2
            )

    priority_weight = task.priority_level.priority_value
    efficiency_with_priority = round(efficiency * priority_weight, 2)

    return efficiency_with_priority


def percentage_tasks_completed_by_priority():
    priority_order = F("priority_level__priority_value")

    completed_before_deadline = Case(
        When(completion_date__lt=F("deadline"), then=1),
        default=0,
        output_field=FloatField(),
    )

    result = (
        Tasks.objects.annotate(
            priority_group=F("priority_level__priority_value"),
            completed=completed_before_deadline,
        )
        .values("priority_group")
        .order_by(priority_order)
        .annotate(
            total_tasks=Count("task_id"),
            completed_tasks=Count("task_id", filter=completed_before_deadline),
        )
    )

    for group in result:
        group["percent_completed"] = (
            group["completed_tasks"] / group["total_tasks"] * 100
            if group["total_tasks"] > 0
            else 0
        )

    return result


def percentage_tasks_completed_by_slidetime():
    priority_order = F("priority_level__priority_value")

    completed_in_slide_time = Case(
        When(completion_date__lt=F("deadline"), then=1),
        When(
            completion_date__gte=F("deadline"),
            completion_date__lte=F("deadline") + F("acceptable_slide_time"),
            then=1,
        ),
        default=0,
        output_field=FloatField(),
    )

    result = (
        Tasks.objects.annotate(
            priority_group=F("priority_level__priority_value"),
            completed=completed_in_slide_time,
        )
        .values("priority_group")
        .order_by(priority_order)
        .annotate(
            total_tasks=Count("task_id"),
            completed_tasks=Count("task_id", filter=completed_in_slide_time),
        )
    )

    for group in result:
        group["percent_completed"] = (
            group["completed_tasks"] / group["total_tasks"] * 100
            if group["total_tasks"] > 0
            else 0
        )

    return result


def percentage_tasks_completed_by_expectedtime():
    priority_order = F("priority_level__priority_value")

    completed_before_expectedtime = Case(
        When(completion_date__lt=F("expected_completion_date"), then=1),
        default=0,
        output_field=FloatField(),
    )

    result = (
        Tasks.objects.annotate(
            priority_group=F("priority_level__priority_value"),
            completed=completed_before_expectedtime,
        )
        .values("priority_group")
        .order_by(priority_order)
        .annotate(
            total_tasks=Count("task_id"),
            completed_tasks=Count("task_id", filter=completed_before_expectedtime),
        )
    )

    for group in result:
        group["percent_completed"] = (
            group["completed_tasks"] / group["total_tasks"] * 100
            if group["total_tasks"] > 0
            else 0
        )

    return result


def calculate_deadline_completion_percentage_by_category_till_now(deadline_now=True):
    if deadline_now:
        current_time = timezone.now()

        tasks = Tasks.objects.filter(deadline__lte=current_time).select_related(
            "task_category__name"
        )
    else:
        tasks = Tasks.objects.all().select_related("task_category__name")
        categories = tasks.values("task_category__name").annotate(
            category_count=Count("task_category__name")
        )

    categories = tasks.values("task_category__name").annotate(
        category_count=Count("task_category__name")
    )

    completed_tasks = tasks.filter(
        Q(completion_date__lte=F("deadline")) | Q(completion_date__isnull=True)
    )
    completed_categories = completed_tasks.values("task_category__name").annotate(
        completed_count=Count("task_category__name")
    )

    percentages = {}
    for category in categories:
        category_id = category["task_category__name"]
        total_count = category["category_count"]
        completed_count = next(
            (
                item["completed_count"]
                for item in completed_categories
                if item["task_category__name"] == category_id
            ),
            0,
        )
        percentage = (
            round((completed_count / total_count) * 100, 2) if total_count > 0 else 0
        )
        percentages[category_id] = percentage

    return percentages


def calculate_slidetime_completion_percentage_by_category_till_now(slidetime_now=True):
    if slidetime_now:
        current_time = timezone.now()

        tasks = Tasks.objects.filter(
            F("acceptable_slide_time") + F("deadline") <= current_time
        ).select_related("task_category__name")
    else:
        tasks = Tasks.objects.all().select_related("task_category__name")
        categories = tasks.values("task_category__name").annotate(
            category_count=Count("task_category__name")
        )

    categories = tasks.values("task_category__name").annotate(
        category_count=Count("task_category__name")
    )

    completed_tasks = tasks.filter(
        Q(completion_date__lte=F("acceptable_slide_time"))
        | Q(completion_date__isnull=True)
    )
    completed_categories = completed_tasks.values("task_category__name").annotate(
        completed_count=Count("task_category__name")
    )

    percentages = {}
    for category in categories:
        category_id = category["task_category__name"]
        total_count = category["category_count"]
        completed_count = next(
            (
                item["completed_count"]
                for item in completed_categories
                if item["task_category__name"] == category_id
            ),
            0,
        )
        percentage = (
            round((completed_count / total_count) * 100, 2) if total_count > 0 else 0
        )
        percentages[category_id] = percentage

    return percentages


def calculate_expectedtime_completion_percentage_by_category_till_now(
    expectedtime_now=True,
):
    if expectedtime_now:
        current_time = timezone.now()

        tasks = Tasks.objects.filter(
            expected_completion_date__lte=current_time
        ).select_related("task_category__name")
    else:
        tasks = Tasks.objects.all().select_related("task_category__name")
        categories = tasks.values("task_category__name").annotate(
            category_count=Count("task_category__name")
        )

    categories = tasks.values("task_category__name").annotate(
        category_count=Count("task_category__name")
    )

    completed_tasks = tasks.filter(
        Q(completion_date__lte=F("expected_completion_date"))
        | Q(completion_date__isnull=True)
    )
    completed_categories = completed_tasks.values("task_category__name").annotate(
        completed_count=Count("task_category__name")
    )

    percentages = {}
    for category in categories:
        category_id = category["task_category__name"]
        total_count = category["category_count"]
        completed_count = next(
            (
                item["completed_count"]
                for item in completed_categories
                if item["task_category"] == category_id
            ),
            0,
        )
        percentage = (
            round((completed_count / total_count) * 100, 2) if total_count > 0 else 0
        )
        percentages[category_id] = percentage

    return percentages


def calculate_average_completion_time_by_category(
    deadline=True, slidetime=False, expectedtime=False
):
    if deadline:
        average_completion_time_by_category = Tasks.objects.values(
            "task_category__name"
        ).annotate(avg_completion_time=Avg(F("completion_date") - F("deadline")))
    elif slidetime:
        average_completion_time_by_category = Tasks.objects.values(
            "task_category__name"
        ).annotate(
            avg_completion_time=Avg(
                F("completion_date") - (F("acceptable_slide_time") + F("deadline"))
            )
        )
    elif expectedtime:
        average_completion_time_by_category = Tasks.objects.values(
            "task_category__name"
        ).annotate(
            avg_completion_time=Avg(
                F("completion_date") - F("expected_completion_date")
            )
        )

    result = {}
    for item in average_completion_time_by_category:
        category = item["task_category__name"]
        result[category] = item["avg_completion_time"]

    return result


def calculate_average_completion_time_by_priority(
    deadline=True, slidetime=False, expectedtime=False
):
    if deadline:
        average_completion_time_by_priority = Tasks.objects.values(
            "priority_level__priority_value"
        ).annotate(avg_completion_time=Avg(F("completion_date") - F("deadline")))
    elif slidetime:
        average_completion_time_by_priority = Tasks.objects.values(
            "priority_level__priority_value"
        ).annotate(
            avg_completion_time=Avg(
                F("completion_date") - (F("acceptable_slide_time") + F("deadline"))
            )
        )
    elif expectedtime:
        average_completion_time_by_priority = Tasks.objects.values(
            "priority_level__priority_value"
        ).annotate(
            avg_completion_time=Avg(
                F("completion_date") - F("expected_completion_date")
            )
        )

    result = {}
    for item in average_completion_time_by_priority:
        category = item["priority_level__priority_value"]
        result[category] = item["avg_completion_time"]

    return result


def calculate_task_time_by_category():
    categories = TaskCategories.objects.all()
    results = []
    for category in categories:
        task_time = (
            Tasks.objects.filter(task_category=category)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((category.name, task_time["total_time"]))
    return results


def calculate_task_time_by_priority():
    priority_levels = PriorityLevels.objects.all()
    results = []
    for priority_level in priority_levels:
        task_time = (
            Tasks.objects.filter(priority_level=priority_level)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((priority_level.priority_value, task_time["total_time"]))
    return results
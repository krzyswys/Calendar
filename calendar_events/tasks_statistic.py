from datetime import timedelta
from calendar_events.models import Tasks, PriorityLevels, TaskCategories
from django.db.models import (
    Sum,
    F,
    Avg,
    Count,
    Q,
    FloatField,
    When,
    Case,
    Value,
    ExpressionWrapper,
    DurationField,
)

zero_date = timedelta(0)


def calculate_efficiency_of_task(task: Tasks):
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


def calculate_efficiency_with_priority_of_task(task):
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


def percentage_tasks_completed_by_priority(
    deadline=True, slidetime=False, expectedtime=False, start_date=None, end_date=None
):
    tasks = Tasks.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)

    priority_order = F("priority_level__priority_value")

    if deadline:
        completed_in_time = Case(
            When(completion_date__lt=F("deadline"), then=1),
            default=0,
            output_field=FloatField(),
        )
    elif slidetime:
        completed_in_time = Case(
            When(completion_date__lt=F("deadline"), then=1),
            When(
                completion_date__gte=F("deadline"),
                completion_date__lte=F("deadline") + F("acceptable_slide_time"),
                then=1,
            ),
            default=0,
            output_field=FloatField(),
        )
    elif expectedtime:
        completed_in_time = Case(
            When(completion_date__lt=F("expected_completion_date"), then=1),
            default=0,
            output_field=FloatField(),
        )

    result = (
        tasks.annotate(
            priority_group=F("priority_level__priority_value"),
            completed=completed_in_time,
        )
        .values("priority_group")
        .order_by(priority_order)
        .annotate(
            total_tasks=Count("task_id"),
            completed_tasks=Count("task_id", filter=completed_in_time),
        )
    )

    for group in result:
        group["percent_completed"] = (
            group["completed_tasks"] / group["total_tasks"] * 100
            if group["total_tasks"] > 0
            else 0
        )
    result_dict = {}
    for item in result:
        result_dict[item["priority_group"]] = item["percent_completed"]
    return result_dict


def calculate_completion_percentage_by_category_till_now(
    deadline=True, slidetime=False, expectedtime=False, start_date=None, end_date=None
):
    tasks = Tasks.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)

    if deadline:
        completed_tasks = tasks.filter(
            Q(completion_date__lte=F("deadline")) | Q(completion_date__isnull=True)
        )
    elif slidetime:
        completed_tasks = tasks.filter(
            Q(completion_date__gte=F("deadline"))
            | Q(completion_date__lte=F("deadline") + F("acceptable_slide_time"))
            | Q(completion_date__isnull=True)
        )
    elif expectedtime:
        completed_tasks = tasks.filter(
            Q(completion_date__lte=F("expected_completion_date"))
            | Q(completion_date__isnull=True)
        )

    categories = TaskCategories.objects.all()

    category_counts = {}
    for task in tasks:
        if task.task_category.name not in category_counts:
            category_counts[task.task_category.name] = 1
        else:
            category_counts[task.task_category.name] += 1

    completed_category_counts = {}
    for task in completed_tasks:
        if task.task_category.name not in completed_category_counts:
            completed_category_counts[task.task_category.name] = 1
        else:
            completed_category_counts[task.task_category.name] += 1

    percentages = {}
    for category in categories:
        category_id = category.name
        total_count = category_counts.get(category_id, 0)
        completed_count = completed_category_counts.get(category_id, 0)
        percentage = (
            round((completed_count / total_count) * 100, 2) if total_count > 0 else 0
        )
        percentages[category_id] = percentage

    return percentages


def calculate_average_completion_time_by_category(
    deadline=True, slidetime=False, expectedtime=False, start_date=None, end_date=None
):
    tasks = Tasks.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
    if deadline:
        average_completion_time_by_category = tasks.values(
            "task_category__name"
        ).annotate(
            avg_completion_time=ExpressionWrapper(
                Case(
                    When(
                        completion_date__isnull=False,
                        then=ExpressionWrapper(
                            Avg(F("completion_date") - F("deadline")),
                            output_field=DurationField(),
                        ),
                    ),
                    default=Value(zero_date),
                ),
                output_field=DurationField(),
            )
        )

    elif slidetime:
        average_completion_time_by_category = tasks.values(
            "task_category__name"
        ).annotate(
            avg_completion_time=ExpressionWrapper(
                Case(
                    When(
                        completion_date__isnull=False,
                        then=ExpressionWrapper(
                            Avg(
                                F("completion_date")
                                - (F("acceptable_slide_time") + F("deadline"))
                            ),
                            output_field=DurationField(),
                        ),
                    ),
                    default=Value(zero_date),
                ),
                output_field=DurationField(),
            )
        )

    elif expectedtime:
        average_completion_time_by_category = tasks.values(
            "task_category__name"
        ).annotate(
            avg_completion_time=ExpressionWrapper(
                Case(
                    When(
                        completion_date__isnull=False,
                        then=ExpressionWrapper(
                            Avg(F("completion_date") - F("expected_completion_date")),
                            output_field=DurationField(),
                        ),
                    ),
                    default=Value(zero_date),
                ),
                output_field=DurationField(),
            )
        )

    result = {}
    for item in average_completion_time_by_category:
        category = item["task_category__name"]
        result[category] = item["avg_completion_time"]

    return result


def calculate_average_completion_time_by_priority(
    deadline=True, slidetime=False, expectedtime=False, start_date=None, end_date=None
):
    tasks = Tasks.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
    if deadline:
        average_completion_time_by_priority = tasks.values(
            "priority_level__priority_value"
        ).annotate(
            avg_completion_time=ExpressionWrapper(
                Case(
                    When(
                        completion_date__isnull=False,
                        then=ExpressionWrapper(
                            Avg(F("completion_date") - F("deadline")),
                            output_field=DurationField(),
                        ),
                    ),
                    default=Value(zero_date),
                ),
                output_field=DurationField(),
            )
        )
    elif slidetime:
        average_completion_time_by_priority = tasks.values(
            "priority_level__priority_value"
        ).annotate(
            avg_completion_time=ExpressionWrapper(
                Case(
                    When(
                        completion_date__isnull=False,
                        then=ExpressionWrapper(
                            Avg(
                                F("completion_date")
                                - (F("acceptable_slide_time") + F("deadline"))
                            ),
                            output_field=DurationField(),
                        ),
                    ),
                    default=Value(zero_date),
                ),
                output_field=DurationField(),
            )
        )
    elif expectedtime:
        average_completion_time_by_priority = tasks.values(
            "priority_level__priority_value"
        ).annotate(
            avg_completion_time=ExpressionWrapper(
                Case(
                    When(
                        completion_date__isnull=False,
                        then=ExpressionWrapper(
                            Avg(F("completion_date") - F("expected_completion_date")),
                            output_field=DurationField(),
                        ),
                    ),
                    default=Value(zero_date),
                ),
                output_field=DurationField(),
            )
        )

    result = {}
    for item in average_completion_time_by_priority:
        category = item["priority_level__priority_value"]
        result[category] = item["avg_completion_time"]

    return result


def calculate_task_time_by_category(start_date=None, end_date=None):
    tasks = Tasks.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
    categories = TaskCategories.objects.all()
    results = []
    for category in categories:
        task_time = (
            tasks.filter(task_category=category)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((category.name, task_time["total_time"] or 0))
    result_dict = {}
    for item, value in results:
        result_dict[item] = value
    return result_dict


def calculate_task_time_by_priority(start_date=None, end_date=None):
    tasks = Tasks.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
    priority_levels = PriorityLevels.objects.all()
    results = []
    for priority_level in priority_levels:
        task_time = (
            tasks.filter(priority_level=priority_level)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((priority_level.priority_value, task_time["total_time"] or 0))
    result_dict = {}
    for item, value in results:
        result_dict[item] = value
    return result_dict

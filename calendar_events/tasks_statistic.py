from datetime import timedelta
from calendar_events.models import Tasks, PriorityLevels, TaskCategories, TaskOccurrences
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

from calendar_events.models.tasks import TaskOccurrences

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
    tasks_occurencies = TaskOccurrences.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
        tasks_occurencies = tasks_occurencies.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
        tasks_occurencies = tasks_occurencies.filter(end_time__lte=end_date)

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

    result_for_occurences = (
        tasks_occurencies.annotate(
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
    merged_result = {}
    for group in result:
        priority_group = group["priority_group"]
        merged_result[priority_group] = {
            "total_tasks": group["total_tasks"],
            "completed_tasks": group["completed_tasks"],
        }

    for group in result_for_occurences:
        priority_group = group["priority_group"]
        if priority_group in merged_result:
            merged_result[priority_group]["total_tasks"] += group["total_tasks"]
            merged_result[priority_group]["completed_tasks"] += group["completed_tasks"]
        else:
            merged_result[priority_group] = {
                "total_tasks": group["total_tasks"],
                "completed_tasks": group["completed_tasks"],
            }
    for priority_group, group_data in merged_result.items():
        group_data["percent_completed"] = (
            group_data["completed_tasks"] / group_data["total_tasks"] * 100
            if group_data["total_tasks"] > 0
            else 0
        )
    result_dict = {}
    for priority_group, group_data in merged_result.items():
        result_dict[priority_group] = group_data["percent_completed"]
    return result_dict


def calculate_completion_percentage_by_category_till_now(
    deadline=True, slidetime=False, expectedtime=False, start_date=None, end_date=None
):
    tasks = Tasks.objects.all()
    tasks_occurencies = TaskOccurrences.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
        tasks_occurencies = tasks_occurencies.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
        tasks_occurencies = tasks_occurencies.filter(end_time__lte=end_date)

    if deadline:
        completed_tasks = tasks.filter(
            Q(completion_date__lte=F("deadline")) | Q(completion_date__isnull=True)
        )
        completed_occurencies = tasks_occurencies.filter(
            Q(completion_date__lte=F("deadline")) | Q(completion_date__isnull=True)
        )
    elif slidetime:
        completed_tasks = tasks.filter(
            Q(completion_date__gte=F("deadline"))
            | Q(completion_date__lte=F("deadline") + F("acceptable_slide_time"))
            | Q(completion_date__isnull=True)
        )
        completed_occurencies = tasks_occurencies.filter(
            Q(completion_date__gte=F("deadline"))
            | Q(completion_date__lte=F("deadline") + F("acceptable_slide_time"))
            | Q(completion_date__isnull=True)
        )
    elif expectedtime:
        completed_tasks = tasks.filter(
            Q(completion_date__lte=F("expected_completion_date"))
            | Q(completion_date__isnull=True)
        )
        completed_occurencies = tasks_occurencies.filter(
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
    for task in tasks_occurencies:
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
    for task in completed_occurencies:
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
    tasks_occurencies = TaskOccurrences.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
        tasks_occurencies = tasks_occurencies.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
        tasks_occurencies = tasks_occurencies.filter(end_time__lte=end_date)
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
            ),
            count=Count("task_id"),
        )
        average_completion_time_by_category_occurences = tasks_occurencies.values(
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
            ),
            count=Count("task_occurrence_id"),
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
            ),
            count=Count("task_id"),
        )
        average_completion_time_by_category_occurences = tasks_occurencies.values(
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
            ),
            count=Count("task_occurrence_id"),
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
            ),
            count=Count("task_id"),
        )
        average_completion_time_by_category_occurences = tasks_occurencies.values(
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
            ),
            count=Count("task_occurrence_id"),
        )

    merged_average_completion_time_by_category = {}
    for item in average_completion_time_by_category:
        category = item["task_category__name"]
        sumtime = item["avg_completion_time"] * item["count"]
        count = item["count"]
        merged_average_completion_time_by_category[category] = {
            "sumtime": sumtime,
            "count": count,
        }
    for item in average_completion_time_by_category_occurences:
        if (
            item["task_category__name"]
            not in merged_average_completion_time_by_category
        ):
            category = item["task_category__name"]
            sumtime = item["avg_completion_time"] * item["count"]
            count = item["count"]
            merged_average_completion_time_by_category[category] = {
                "sumtime": sumtime,
                "count": count,
            }
        else:
            category = item["task_category__name"]
            sumtime = (
                item["avg_completion_time"] * item["count"]
                + merged_average_completion_time_by_category[category]["sumtime"]
            )
            count = (
                item["count"]
                + merged_average_completion_time_by_category[category]["count"]
            )
            merged_average_completion_time_by_category[category] = {
                "sumtime": sumtime,
                "count": count,
            }

    result_dict = {}
    for category, group_data in merged_average_completion_time_by_category.items():
        result_dict[category] = group_data["sumtime"] / group_data["count"]
    return result_dict


def calculate_average_completion_time_by_priority(
    deadline=True, slidetime=False, expectedtime=False, start_date=None, end_date=None
):
    tasks = Tasks.objects.all()
    tasks_occurencies = TaskOccurrences.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
        tasks_occurencies = tasks_occurencies.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
        tasks_occurencies = tasks_occurencies.filter(end_time__lte=end_date)
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
            ),
            count=Count("task_id"),
        )
        average_completion_time_by_priority_occurrences = tasks_occurencies.values(
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
            ),
            count=Count("task_occurrence_id"),
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
            ),
            count=Count("task_id"),
        )
        average_completion_time_by_priority_occurrences = tasks_occurencies.values(
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
            ),
            count=Count("task_occurrence_id"),
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
            ),
            count=Count("task_id"),
        )
        average_completion_time_by_priority_occurrences = tasks_occurencies.values(
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
            ),
            count=Count("task_occurrence_id"),
        )

    merged_average_completion_time_by_category = {}
    for item in average_completion_time_by_priority:
        category = item["priority_level__priority_value"]
        sumtime = item["avg_completion_time"] * item["count"]
        count = item["count"]
        merged_average_completion_time_by_category[category] = {
            "sumtime": sumtime,
            "count": count,
        }
    for item in average_completion_time_by_priority_occurrences:
        if (
            item["priority_level__priority_value"]
            not in merged_average_completion_time_by_category
        ):
            category = item["priority_level__priority_value"]
            sumtime = item["avg_completion_time"] * item["count"]
            count = item["count"]
            merged_average_completion_time_by_category[category] = {
                "sumtime": sumtime,
                "count": count,
            }
        else:
            category = item["priority_level__priority_value"]
            sumtime = (
                item["avg_completion_time"] * item["count"]
                + merged_average_completion_time_by_category[category]["sumtime"]
            )
            count = (
                item["count"]
                + merged_average_completion_time_by_category[category]["count"]
            )
            merged_average_completion_time_by_category[category] = {
                "sumtime": sumtime,
                "count": count,
            }

    result_dict = {}
    for category, group_data in merged_average_completion_time_by_category.items():
        result_dict[category] = group_data["sumtime"] / group_data["count"]
    return result_dict


def calculate_task_time_by_category(start_date=None, end_date=None):
    tasks = Tasks.objects.all()
    tasks_occurencies = TaskOccurrences.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
        tasks_occurencies = tasks_occurencies.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
        tasks_occurencies = tasks_occurencies.filter(end_time__lte=end_date)
    categories = TaskCategories.objects.all()
    results = []
    for category in categories:
        task_time = (
            tasks.filter(task_category=category)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((category.name, task_time["total_time"] or 0))
        task_time = (
            tasks_occurencies.filter(task_category=category)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((category.name, task_time["total_time"] or 0))
    result_dict = {}
    for item, value in results:
        if item not in result_dict:
            result_dict[item] = value
        else:
            result_dict[item] += value
    return result_dict


def calculate_task_time_by_priority(start_date=None, end_date=None):
    tasks = Tasks.objects.all()
    tasks_occurencies = TaskOccurrences.objects.all()
    if start_date:
        tasks = tasks.filter(start_time__gte=start_date)
        tasks_occurencies = tasks_occurencies.filter(start_time__gte=start_date)
    if end_date:
        tasks = tasks.filter(end_time__lte=end_date)
        tasks_occurencies = tasks_occurencies.filter(end_time__lte=end_date)
    priority_levels = PriorityLevels.objects.all()
    results = []
    for priority_level in priority_levels:
        task_time = (
            tasks.filter(priority_level=priority_level)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((priority_level.priority_value, task_time["total_time"] or 0))
        task_time = (
            tasks_occurencies.filter(priority_level=priority_level)
            .annotate(time_taken=F("completion_date") - F("creation_date"))
            .aggregate(total_time=Sum("time_taken"))
        )
        results.append((priority_level.priority_value, task_time["total_time"] or 0))
    result_dict = {}
    for item, value in results:
        if item not in result_dict:
            result_dict[item] = value
        else:
            result_dict[item] += value
    return result_dict


#Returns time taken by a task with its all subtasks
def calculate_time_spend_with_subtasks(task: Tasks, start_date=None, end_date=None):
    tasks = task.get_all_subtasks()

    task_occurrences = TaskOccurrences.get_task_occurrences(task__in=tasks)

    if start_date is not None:
        task_occurrences.filter(start_time__gte=start_date)

    if end_date is not None:
        task_occurrences.filter(start_date__lte=end_date)

    time = task_occurrences.annotate(time_taken=F("completion_date") - F("creation_date")).aggregate(total_time=Sum("time_taken"))

    return time['total_time']


#Returns task completion in percents (calculated by counting done subtasks)
def calculate_task_completion_with_subtasks(task: Tasks):
    tasks = task.get_all_subtasks()

    task_occurrences = TaskOccurrences.get_task_occurrences(task__in=tasks)

    all_tasks_number = len(task_occurrences)

    task_occurrences.filter(status=1)

    finished_tasks_number = len(task_occurrences)

    return (finished_tasks_number / all_tasks_number) * 100


#Returns tuple with 4 numbers measuring completion date: before expected completion time, before expected + slide time, before deadline, after deadline.
#Counters do not stack: if a task was completed before expected time (so it was also completed before expected + slide, deadline...) only the first counter is incremented.
def calculate_completion_number_by_completion_time_with_subtasks(task: Tasks):
    tasks = task.get_all_subtasks()

    task_occurrences = TaskOccurrences.get_task_occurrences(task__in=tasks)

    expected_time = 0
    slide_time = 0
    deadline = 0
    after_deadline = 0

    for task in task_occurrences:
        if task.completion_date is None:
            continue

        if task.completion_date <= task.expected_completion_date:
            expected_time += 1
        elif task.completion_date <= task.expected_completion_date + task.acceptable_slide_time:
            slide_time += 1
        elif task.completion_date <= task.deadline:
            deadline += 1
        else:
            after_deadline += 1

    return expected_time, slide_time, deadline, after_deadline


#Returns average expected_completion_date - completion_date for subtasks which were completed before expected date
def calculate_mean_completion_before_expected_time_with_subtasks(task: Tasks):
    tasks = task.get_all_subtasks()

    task_occurrences = TaskOccurrences.get_task_occurrences(task__in=tasks).filter(completion_date__isnull=False).filter(completion_date__lte=F('expected_completion_date'))

    time = task_occurrences.annotate(time_taken=F("expected_completion_date") - F("completion_date")).aggregate(total_time=Avg("time_taken"))

    return time['total_time']

#Returns average (expected_completion_date + slide_time) - completion_date for subtasks, which were completed before expected_date + slide and after expected_date
def calculate_mean_completion_before_expected_time_plus_slide_with_subtasks(task: Tasks):
    tasks = task.get_all_subtasks()

    task_occurrences = TaskOccurrences.get_task_occurrences(task__in=tasks).filter(completion_date__isnull=False)\
        .filter(completion_date__lte=(F('expected_completion_date') + F('acceptable_slide_time')))\
        .filter(completion_date__gt=F('expected_completion_date'))

    time = task_occurrences.annotate(time_taken=(F('expected_completion_date') + F('acceptable_slide_time')) - F("completion_date")).aggregate(total_time=Avg("time_taken"))

    return time['total_time']

#Returns average deadline - completion_date for subtasks, which were completed before deadline and after expected_date + slide
def calculate_mean_completion_before_deadline_with_subtasks(task: Tasks):
    tasks = task.get_all_subtasks()

    task_occurrences = TaskOccurrences.get_task_occurrences(task__in=tasks).filter(completion_date__isnull=False)\
        .filter(completion_date__lte=F('deadline'))\
        .filter(completion_date__gt=(F('expected_completion_date') + F('acceptable_slide_time')))

    time = task_occurrences.annotate(time_taken=F('deadline') - F("completion_date")).aggregate(total_time=Avg("time_taken"))

    return time['total_time']


#Returns average completion_date - deadline for subtasks, which were completed after the deadline
def calculate_mean_completion_after_deadline_with_subtasks(task: Tasks):
    tasks = task.get_all_subtasks()

    task_occurrences = TaskOccurrences.get_task_occurrences(task__in=tasks).filter(completion_date__isnull=False)\
        .filter(completion_date__gt=F('deadline'))

    time = task_occurrences.annotate(time_taken=F('completion_date') - F("deadline")).aggregate(total_time=Avg("time_taken"))

    return time['total_time']
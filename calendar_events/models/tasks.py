from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import exceptions as e
from calendar_events.models.users import Users
from calendar_events.models.priorityLevels import PriorityLevels
from calendar_events.models.repeatPattern import RepeatPatterns
from calendar_events.models.taskCategories import TaskCategories


class Tasks(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    task_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    task_category = models.ForeignKey(TaskCategories, on_delete=models.CASCADE)
    priority_level = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    repeat_pattern = models.ForeignKey(RepeatPatterns, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500)
    reminder_time = models.DurationField()
    localization = models.CharField(max_length=60)
    creation_date = models.DateTimeField(default=datetime.now)
    color = models.CharField(max_length=3)
    expected_completion_date = models.DateTimeField()
    deadline = models.DateTimeField()
    acceptable_slide_time = models.DurationField()
    first_occurrence = models.DateTimeField()
    completion_date = models.DateTimeField(null=True)

    class StatusOptions(models.IntegerChoices):
        (0, "Not finished"),
        (1, "Finished"),
        (-1, "Not aplicable")

    status = models.IntegerField(choices=StatusOptions, blank=True, null=True)

    def __str__(self):
        return self.Name

    @staticmethod
    def create_task(
        user: Users,
        task_category: TaskCategories,
        priority_level: PriorityLevels,
        repeat_pattern: RepeatPatterns,
        name: str,
        expected_completion_date: datetime,
        first_occurrence: datetime,
        description: str = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
        deadline: datetime = None,
        acceptable_slide_time: timedelta = None,
        completion_time: datetime = None,
    ):
        task = Tasks()
        task.task_creator = user
        task.task_category = task_category
        task.priority_level = priority_level
        task.repeat_pattern = repeat_pattern
        task.name = name
        task.expected_completion_date = expected_completion_date
        task.first_occurrence = first_occurrence
        # task.status = 0

        if description is None:
            task.description = ""
        else:
            task.description = description

        if reminder_time is None:
            task.reminder_time = task_category.default_reminder_time
        else:
            task.reminder_time = reminder_time

        if localization is None:
            task.localization = task_category.default_localization
        else:
            task.localization = localization

        if color is None:
            task.color = task_category.default_color
        else:
            task.color = color

        if deadline is None:
            task.deadline = task_category.default_deadline
        else:
            task.deadline = deadline

        if acceptable_slide_time is None:
            task.acceptable_slide_time = task_category.default_acceptable_slide_time
        else:
            task.acceptable_slide_time = acceptable_slide_time
        if completion_time is not None:
            task.acceptable_slide_time = completion_time
            task.status = 1

        try:
            task.save()
            return task
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create task")

    @staticmethod
    def get_tasks(
        task_id: int = None,
        user: Users = None,
        name: str = None,
        category: TaskCategories = None,
        localization: str = None,
        expected_completion_date: datetime = None,
        deadline: datetime = None,
    ):
        try:
            all_tasks = Tasks.objects.all()

            if task_id is not None:
                all_tasks.filter(task_id=task_id)

            if user is not None:
                all_tasks.filter(task_creator=user)

            if name is not None:
                all_tasks.filter(name=name)

            if category is not None:
                all_tasks.filter(task_category=category)

            if localization is not None:
                all_tasks.filter(localization=localization)

            if expected_completion_date is not None:
                all_tasks.filter(expected_completion_date=expected_completion_date)

            if deadline is not None:
                all_tasks.filter(deadline=deadline)

            return all_tasks
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find such task")

    def modify(
        self,
        name: str = None,
        category: TaskCategories = None,
        priority_level: PriorityLevels = None,
        repeat_pattern: RepeatPatterns = None,
        description: str = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
        expected_completion_date: datetime = None,
        deadline: datetime = None,
        acceptable_slide_time: timedelta = None,
        completion_time: datetime = None,
    ):
        if name is not None:
            self.name = name

        if category is not None:
            self.task_category = category

        if priority_level is not None:
            self.priority_level = priority_level

        if repeat_pattern is not None:
            self.repeat_pattern = repeat_pattern

        if description is not None:
            self.description = description

        if reminder_time is not None:
            self.reminder_time = reminder_time

        if localization is not None:
            self.localization = localization

        if color is not None:
            self.color = color

        if expected_completion_date is not None:
            self.expected_completion_date = expected_completion_date

        if deadline is not None:
            self.deadline = deadline

        if acceptable_slide_time is not None:
            self.acceptable_slide_time = acceptable_slide_time
        if completion_time is not None:
            self.completion_date = completion_time
            self.status = 1

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save task")

    def check_task_done(
        self,
        date: datetime = None,
    ):
        if date is not None:
            self.completion_date = date
        else:
            self.completion_date = datetime.now()
        self.status = 1
        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save task")

    @staticmethod
    def apply_task_pattern_for(task):
        repeat_pattern = task.repeat_pattern

        start_date = task.first_occurrence

        for i in range(repeat_pattern.number_of_repetitions):
            start_date += relativedelta(
                years=repeat_pattern.years_interval,
                months=repeat_pattern.months_interval,
                weeks=repeat_pattern.weeks_interval,
                days=repeat_pattern.days_interval,
            )
            occurrence = TaskOccurrences.create_task_occurrence(
                task=task, start_time=start_date
            )


class TaskOccurrences(models.Model):
    task_occurrence_id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    task_creator = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    task_category = models.ForeignKey(
        TaskCategories, on_delete=models.CASCADE, null=True
    )
    priority_level = models.ForeignKey(
        PriorityLevels, on_delete=models.CASCADE, null=True
    )
    repeat_pattern = models.ForeignKey(
        RepeatPatterns, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=60, null=True)
    description = models.CharField(max_length=500, null=True)
    reminder_time = models.DurationField(null=True)
    localization = models.CharField(max_length=60, null=True)
    creation_date = models.DateTimeField(default=datetime.now, null=True)
    color = models.CharField(max_length=3, null=True)
    expected_completion_date = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)
    acceptable_slide_time = models.DurationField(null=True)
    first_occurrence = models.DateTimeField(null=True)
    completion_date = models.DateTimeField(null=True)

    class StatusOptions(models.IntegerChoices):
        (0, "Not finished"),
        (1, "Finished"),
        (-1, "Not aplicable")

    status = models.IntegerField(choices=StatusOptions, blank=True, null=True)

    @staticmethod
    def create_task_occurrence(task: Tasks, start_time: datetime):
        task_occurrence = TaskOccurrences()
        task_occurrence.task = task
        task_occurrence.start_time = start_time
        task_occurrence.task_creator = task.task_creator
        task_occurrence.task_category = task.task_category
        task_occurrence.priority_level = task.priority_level
        task_occurrence.repeat_pattern = task.repeat_pattern
        task_occurrence.name = task.name
        task_occurrence.description = task.description
        task_occurrence.reminder_time = task.reminder_time
        task_occurrence.localization = task.localization
        task_occurrence.creation_date = datetime.now()
        task_occurrence.color = task.color
        task_occurrence.expected_completion_date = task.expected_completion_date
        task_occurrence.deadline = task.deadline
        task_occurrence.acceptable_slide_time = task.acceptable_slide_time
        task_occurrence.first_occurrence = task.first_occurrence

        try:
            task_occurrence.save()
            return task_occurrence
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create task occurrence")

    @staticmethod
    def get_task_occurrences(
        task_occurrence_id: int,
        task: Tasks,
        time_start: datetime,
        time_stop: datetime,
    ):
        try:
            all_occurrences = TaskOccurrences.objects.all()

            if task_occurrence_id is not None:
                all_occurrences.filter(task_occurrence_id=task_occurrence_id)

            if task is not None:
                all_occurrences.filter(task=task)

            if time_start is not None:
                all_occurrences.filter(start_time__gte=time_start)

            if time_stop is not None:
                all_occurrences.filter(start_time__lte=time_stop)

            return all_occurrences

        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find such task occurrence")

    def modify(
        self,
        task: Tasks = None,
        name: str = None,
        category: TaskCategories = None,
        priority_level: PriorityLevels = None,
        repeat_pattern: RepeatPatterns = None,
        description: str = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
        expected_completion_date: datetime = None,
        deadline: datetime = None,
        acceptable_slide_time: timedelta = None,
        completion_time: datetime = None,
    ):
        if task is not None:
            self.task = task
        if name is not None:
            self.name = name

        if category is not None:
            self.task_category = category

        if priority_level is not None:
            self.priority_level = priority_level
        if repeat_pattern is not None:
            self.repeat_pattern = repeat_pattern

        if description is not None:
            self.description = description

        if reminder_time is not None:
            self.reminder_time = reminder_time

        if localization is not None:
            self.localization = localization

        if color is not None:
            self.color = color

        if expected_completion_date is not None:
            self.expected_completion_date = expected_completion_date

        if deadline is not None:
            self.deadline = deadline

        if acceptable_slide_time is not None:
            self.acceptable_slide_time = acceptable_slide_time
        if completion_time is not None:
            self.completion_date = completion_time
            self.status = 1
        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save task occurrence")

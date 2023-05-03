from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import calendar_events.models as md
import exceptions as e

from django.shortcuts import render

# FIXME: set as default/none categories,priority levels, reapetpatterns ...
# TODO: add status field as optional when creating new task
# TODO: add standard duration for task_category: sysopy->kolejny tydzień
# TODO: create subtasks logic
# TODO: measurments for substasks + task_occurences
# TODO: add abiility to set completion_date of task in past
# TODO: subcategories for events?


def index(request):
    users = Users.objects.all()
    priority_levels = PriorityLevels.objects.all()
    event_categories = EventCategories.objects.all()
    repeat_patterns = RepeatPatterns.objects.all()
    events = Events.objects.all()
    task_categories = TaskCategories.objects.all()
    tasks = Tasks.objects.all()
    notes = Notes.objects.all()
    event_occurences = EventOccurrences.objects.all()
    tasks_occurences = TaskOccurrences.objects.all()
    context = {
        "users": users,
        "priority_levels": priority_levels,
        "event_categories": event_categories,
        "repeat_patterns": repeat_patterns,
        "events": events,
        "task_categories": task_categories,
        "tasks": tasks,
        "notes": notes,
        "event_occurences": event_occurences,
        "tasks_occurences": tasks_occurences,
    }

    return render(request, "index.html", context)


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    login = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.login

    @staticmethod
    def create_user(login: str):
        if login is None:
            raise e.NoDataGiven("Login cannot be None")

        user = md.Users()
        user.login = login

        try:
            user.save()
            return user
        except IntegrityError:
            raise e.EntityAlreadyExists("User with specified login already exists")

    @staticmethod
    def get_user(user_id: int = None, login: str = None):
        if user_id is None and login is None:
            raise e.NoDataGiven("Need to specify id or login")

        try:
            if user_id is not None:
                return md.Users.objects.get(user_id=user_id)
            else:
                return md.Users.objects.get(login=login)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified user")

    def modify(self, new_login: str):
        if new_login is None:
            raise e.NoDataGiven("Login cannot be None")

        self.login = new_login

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("User with specified login already exists!")


class PriorityLevels(models.Model):
    priority_level_id = models.BigAutoField(primary_key=True)
    priority_level_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    priority_value = models.IntegerField()
    markdown = models.CharField(max_length=1, blank=True)
    default_reminder_time = models.DurationField()

    def __str__(self):
        return self.name

    @staticmethod
    def create_priority_level(
        user: md.Users,
        name: str,
        priority: int,
        default_reminder_time: timedelta,
        markdown: str = None,
    ):
        if (
            user is None
            or name is None
            or priority is None
            or default_reminder_time is None
        ):
            raise e.NoDataGiven("Need to specify all needed values")

        priority_level = md.PriorityLevels()
        priority_level.priority_level_creator = user
        priority_level.name = name
        priority_level.priority_value = priority
        priority_level.default_reminder_time = default_reminder_time

        if markdown is None:
            priority_level.markdown = ""
        else:
            priority_level.markdown = markdown

        try:
            priority_level.save()
            return priority_level
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create priority level")

    @staticmethod
    def get_priority_levels(
        pr_id: int = None, pr_name: str = None, user: md.Users = None, value=None
    ):
        if pr_id is None and pr_name is None and user is None and value is None:
            raise e.NoDataGiven("Need to specify some values")

        try:
            if pr_id is not None:
                return md.PriorityLevels.objects.get(priority_level_id=pr_id)
            elif pr_name is not None:
                return md.PriorityLevels.objects.get(name=pr_name)
            elif value is not None:
                return md.PriorityLevels.objects.get(priority_value=value)
            else:
                return md.PriorityLevels.objects.get(priority_level_creator=user.User)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified priority level")

    def modify(
        self,
        name: str = None,
        priority: int = None,
        markdown: str = None,
        default_reminder_time: timedelta = None,
    ):
        if name is not None:
            self.name = name

        if priority is not None:
            self.priority_value = priority

        if markdown is not None:
            self.markdown = markdown

        if default_reminder_time is not None:
            self.default_reminder_time = default_reminder_time

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save priority level")


class EventCategories(models.Model):
    event_category_id = models.BigAutoField(primary_key=True)
    event_category_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500, blank=True)
    default_priority_level = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    default_reminder_time = models.DurationField()
    default_localization = models.CharField(max_length=60, blank=True)
    default_duration_time = models.DurationField()
    default_color = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create_event_category(
        user: md.Users,
        name: str,
        default_priority_level: md.PriorityLevels,
        default_duration_time: timedelta,
        description: str = None,
        default_localization: str = None,
        default_color: str = None,
        default_reminder_time: timedelta = None,
    ):
        event_category = md.EventCategories()
        event_category.event_category_creator = user
        event_category.name = name
        event_category.default_priority_level = default_priority_level
        event_category.default_duration_time = default_duration_time

        if description is not None:
            event_category.description = description
        else:
            event_category.description = ""

        if default_localization is not None:
            event_category.default_localization = default_localization
        else:
            event_category.default_localization = ""

        if default_color is not None:
            event_category.default_color = default_color
        else:
            event_category.default_color = "FFFFFF"

        if default_reminder_time is not None:
            event_category.default_reminder_time = default_reminder_time
        else:
            event_category.default_reminder_time = (
                default_priority_level.DefaultReminderTime
            )

        try:
            event_category.save()
            return event_category
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create event category")

    @staticmethod
    def get_event_category(cat_id: int = None, cat_name: str = None):
        if cat_id is None and cat_name is None:
            raise e.NoDataGiven("Need to specify some values")

        try:
            if cat_id is not None:
                return md.EventCategories.objects.get(event_categeory_id=cat_id)
            else:
                return md.EventCategories.objects.get(name=cat_name)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified event category")

    def modify(
        self,
        name: str = None,
        description: str = None,
        default_priority_level: md.PriorityLevels = None,
        default_localization: str = None,
        default_duration_time: timedelta = None,
        default_color: str = None,
        default_reminder_time: timedelta = None,
    ):
        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if default_priority_level is not None:
            self.default_priority_level = default_priority_level

        if default_localization is not None:
            self.default_localization = default_localization

        if default_duration_time is not None:
            self.default_duration_time = default_duration_time

        if default_color is not None:
            self.default_color = default_color

        if default_reminder_time is not None:
            self.default_reminder_time = default_reminder_time

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save event category")


class RepeatPatterns(models.Model):
    repeat_pattern_id = models.BigAutoField(primary_key=True)
    repeat_pattern_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    days_interval = models.IntegerField()
    weeks_interval = models.IntegerField()
    months_interval = models.IntegerField()
    years_interval = models.IntegerField()
    number_of_repetitions = models.IntegerField()

    def __str__(self):
        return self.name

    @staticmethod
    def create_repeat_pattern(
        user: md.Users,
        name: str,
        days_interval: int,
        weeks_interval: int,
        months_interval: int,
        years_interval: int,
        number_of_repetitions: int = 1,
    ):
        repeat_pattern = md.RepeatPatterns()
        repeat_pattern.repeat_pattern_creator = user
        repeat_pattern.name = name
        repeat_pattern.days_interval = days_interval
        repeat_pattern.weeks_interval = weeks_interval
        repeat_pattern.months_interval = months_interval
        repeat_pattern.years_interval = years_interval
        repeat_pattern.number_of_repetitions = number_of_repetitions

        if number_of_repetitions < 1:
            raise e.WrongNewData("Number of repetitions must be greater or equal to 1")

        try:
            repeat_pattern.save()
            return repeat_pattern
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create repeat pattern")

    @staticmethod
    def get_repeat_pattern(rp_id: int = None, rp_name: str = None):
        if rp_id is None and rp_name is None:
            raise e.NoDataGiven("Need to specify some values")

        try:
            if rp_id is not None:
                return md.RepeatPatterns.objects.get(repeat_pattern_id=rp_id)
            else:
                return md.RepeatPatterns.objects.get(name=rp_name)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified repeat pattern")

    def modify(
        self,
        name: str = None,
        days_interval: int = None,
        weeks_interval: int = None,
        months_interval: int = None,
        years_interval: int = None,
        number_of_repetitions: int = None,
    ):
        if name is not None:
            self.name = name

        if days_interval is not None:
            self.days_interval = days_interval

        if weeks_interval is not None:
            self.weeks_interval = weeks_interval

        if months_interval is not None:
            self.months_interval = months_interval

        if years_interval is not None:
            self.years_interval = years_interval

        if number_of_repetitions is not None:
            self.number_of_repetitions = number_of_repetitions

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save repeat pattern")


class Events(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    event_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    event_category = models.ForeignKey(EventCategories, on_delete=models.CASCADE)
    priority_level = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    repeat_pattern = models.ForeignKey(RepeatPatterns, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500)
    reminder_time = models.DurationField()
    localization = models.CharField(max_length=60)
    duration = models.DurationField()
    creation_date = models.DateTimeField(default=datetime.now)
    color = models.CharField(max_length=3)
    first_occurrence = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    @staticmethod
    def create_event(
        user: md.Users,
        event_category: md.EventCategories,
        name: str,
        repeat_pattern: md.RepeatPatterns,
        first_occurrence: datetime,
        description: str = None,
        duration: timedelta = None,
        priority_level: md.PriorityLevels = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
    ):
        event = md.Events()
        event.event_creator = user
        event.event_category = event_category
        event.repeat_pattern = repeat_pattern
        event.name = name
        event.first_occurrence = first_occurrence
        event.priority_level = priority_level

        if description is None:
            event.description = ""
        else:
            event.description = description

        if duration is None:
            event.duration = event_category.default_duration_time
        else:
            event.duration = duration

        if priority_level is None:
            event.priority_level = event_category.default_priority_level
        else:
            event.priority_level = priority_level

        if reminder_time is None:
            event.reminder_time = event_category.default_reminder_time
        else:
            event.reminder_time = reminder_time

        if localization is None:
            event.localization = event_category.default_localization
        else:
            event.localization = localization

        if color is None:
            event.color = event_category.default_color
        else:
            event.color = color

        try:
            event.save()
            return event
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create event")

    @staticmethod
    def get_events(
        event_id: int = None,
        event_name: str = None,
        event_category: md.EventCategories = None,
        user: md.Users = None,
    ):
        if (
            event_id is None
            and event_name is None
            and event_category is None
            and user is None
        ):
            raise e.NoDataGiven("Need to specify some values")

        try:
            if event_id is not None:
                return md.Events.objects.get(event_id=event_id)
            elif event_name is not None:
                return md.Events.objects.get(name=event_name)
            else:
                all_rows = md.Events.objects.all()

                if event_category is not None:
                    all_rows = all_rows.filter(event_category=event_category)

                if user is not None:
                    all_rows = all_rows.filter(event_creator=user)

                return all_rows
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified event")

    def modify(
        self,
        event_category: md.EventCategories = None,
        name: str = None,
        description: str = None,
        duration: timedelta = None,
        repeat_pattern: md.RepeatPatterns = None,
        priority_level: md.PriorityLevels = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
    ):
        if event_category is not None:
            self.event_category = event_category

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if duration is not None:
            self.duration = duration

        if repeat_pattern is not None:
            self.repeat_pattern = repeat_pattern

        if priority_level is not None:
            self.priority_level = priority_level

        if reminder_time is not None:
            self.reminder_time = reminder_time

        if localization is not None:
            self.localization = localization

        if color is not None:
            self.color = color

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save event")

    @staticmethod
    def apply_event_pattern_for(event):
        repeat_pattern = event.repeat_pattern

        start_date = event.first_occurrence

        for i in range(repeat_pattern.number_of_repetitions):
            occurrence = EventOccurrences.create_event_occurrence(
                event=event, start_time=start_date
            )

            start_date += relativedelta(
                years=repeat_pattern.years_interval,
                months=repeat_pattern.months_interval,
                weeks=repeat_pattern.weeks_interval,
                days=repeat_pattern.days_interval,
            )


class EventOccurrences(models.Model):
    event_occurrence_id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    @staticmethod
    def create_event_occurrence(event: md.Events, start_time: datetime):
        event_occurrence = md.EventOccurrences()
        event_occurrence.event = event
        event_occurrence.start_time = start_time

        try:
            event_occurrence.save()
            return event_occurrence
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create event occurrence")

    @staticmethod
    def get_event_occurrences(
        id_event_occurrence: int = None,
        event: md.Events = None,
        time_start=None,
        time_stop=None,
    ):
        if (
            event is None
            and id_event_occurrence is None
            and time_start is None
            and time_stop is None
        ):
            raise e.NoDataGiven("Need to specify event occurrence")

        try:
            all_occurrences = md.EventOccurrences.objects.all()
            if id_event_occurrence is not None:
                all_occurrences.filter(event_occurrence_id=id_event_occurrence)

            if event is not None:
                all_occurrences.filter(event=event)

            if time_start is not None:
                all_occurrences.filter(start_time__gte=time_start)

            if time_stop is not None:
                all_occurrences.filter(start_time__lte=time_stop)

            return all_occurrences
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified event occurrences")

    def modify(self, event: md.Events = None):
        if event is not None:
            self.event = event

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save event occurrence")


class TaskCategories(models.Model):
    task_category_id = models.BigAutoField(primary_key=True)
    task_category_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500)
    default_priority_level = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    default_reminder_time = models.DurationField()
    default_localization = models.CharField(max_length=60)
    default_color = models.CharField(max_length=6)
    default_acceptable_slide_time = models.DurationField()

    def __str__(self):
        return self.name

    @staticmethod
    def create_task_category(
        user: md.Users,
        name: str,
        default_priority_level: md.PriorityLevels,
        default_acceptable_slide_time: timedelta,
        description: str = None,
        default_reminder_time: timedelta = None,
        default_localization: str = None,
        default_color: str = None,
    ):
        task_category = md.TaskCategories()
        task_category.task_category_creator = user
        task_category.name = name
        task_category.default_priority_level = default_priority_level
        task_category.default_acceptable_slide_time = default_acceptable_slide_time

        if description is None:
            task_category.description = ""
        else:
            task_category.description = description

        if default_reminder_time is None:
            task_category.default_reminder_time = (
                default_priority_level.default_reminder_time
            )
        else:
            task_category.default_reminder_time = default_reminder_time

        if default_localization is None:
            task_category.default_localization = ""
        else:
            task_category.default_localization = default_localization

        if default_color is None:
            task_category.default_color = "FFFFFF"
        else:
            task_category.default_color = default_color

        try:
            task_category.save()
            return task_category
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create task category")

    @staticmethod
    def get_task_categories(
        task_category_id: int = None, user: md.Users = None, name: str = None
    ):
        if task_category_id is None and user is None and name is None:
            raise e.NoDataGiven("Need to specify task category")

        try:
            if task_category_id is not None:
                return md.TaskCategories.objects.get(task_category_id=task_category_id)
            elif user is not None:
                return md.TaskCategories.objects.get(task_category_creator=user)
            else:
                return md.TaskCategories.objects.get(name=name)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified task category")

    def modify(
        self,
        name: str = None,
        description: str = None,
        default_priority_level: md.PriorityLevels = None,
        default_acceptable_slide_time: timedelta = None,
        default_reminder_time: timedelta = None,
        default_localization: str = None,
        default_color: str = None,
    ):
        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if default_priority_level is not None:
            self.default_priority_level = default_priority_level

        if default_acceptable_slide_time is not None:
            self.default_acceptable_slide_time = default_acceptable_slide_time

        if default_reminder_time is not None:
            self.default_reminder_time = default_reminder_time

        if default_localization is not None:
            self.default_localization = default_localization

        if default_color is not None:
            self.default_color = default_color

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save task category")


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

    status = models.IntegerField(choices=StatusOptions)

    def __str__(self):
        return self.Name

    @staticmethod
    def create_task(
        user: md.Users,
        task_category: md.TaskCategories,
        priority_level: md.PriorityLevels,
        repeat_pattern: md.RepeatPatterns,
        name: str,
        expected_completion_date: datetime,
        first_occurrence: datetime,
        description: str = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
        deadline: datetime = None,
        acceptable_slide_time: timedelta = None,
    ):
        task = md.Tasks()
        task.task_creator = user
        task.task_category = task_category
        task.priority_level = priority_level
        task.repeat_pattern = repeat_pattern
        task.name = name
        task.expected_completion_date = expected_completion_date
        task.first_occurrence = first_occurrence
        task.status = 0

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
            task.deadline = expected_completion_date
        else:
            task.deadline = deadline

        if acceptable_slide_time is None:
            task.acceptable_slide_time = task_category.default_acceptable_slide_time
        else:
            task.acceptable_slide_time = acceptable_slide_time

        try:
            task.save()
            return task
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create task")

    @staticmethod
    def get_tasks(
        task_id: int = None,
        user: md.Users = None,
        name: str = None,
        category: md.TaskCategories = None,
        localization: str = None,
        expected_completion_date: datetime = None,
        deadline: datetime = None,
    ):
        try:
            all_tasks = md.Tasks.objects.all()

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
        category: md.TaskCategories = None,
        priority_level: md.PriorityLevels = None,
        repeat_pattern: md.RepeatPatterns = None,
        description: str = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
        expected_completion_date: datetime = None,
        deadline: datetime = None,
        acceptable_slide_time: timedelta = None,
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
            occurrence = TaskOccurrences.create_task_occurrence(
                task=task, start_time=start_date
            )

            start_date += relativedelta(
                years=repeat_pattern.years_interval,
                months=repeat_pattern.months_interval,
                weeks=repeat_pattern.weeks_interval,
                days=repeat_pattern.days_interval,
            )


class TaskOccurrences(models.Model):
    task_occurrence_id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    @staticmethod
    def create_task_occurrence(task: md.Tasks, start_time: datetime):
        task_occurrence = md.TaskOccurrences()
        task_occurrence.task = task
        task_occurrence.start_time = start_time

        try:
            task_occurrence.save()
            return task_occurrence
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create task occurrence")

    @staticmethod
    def get_task_occurrences(
        task_occurrence_id: int,
        task: md.Tasks,
        time_start: datetime,
        time_stop: datetime,
    ):
        try:
            all_occurrences = md.TaskOccurrences.objects.all()

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

    def modify(self, task: md.Tasks = None):
        if task is not None:
            self.task = task

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save task occurrence")


class Notes(models.Model):
    note_id = models.BigAutoField(primary_key=True)
    note_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=4000)
    content = models.CharField(max_length=4000)
    creation_date = models.DateTimeField(default=datetime.now)
    modification_date = models.DateTimeField(default=datetime.now)
    priority_level = models.ForeignKey(
        PriorityLevels, on_delete=models.CASCADE, null=True
    )

    @staticmethod
    def create_note(creator: md.Users, title, content=None, priority_level=None):
        note = md.Notes()
        note.note_creator = creator
        note.title = title

        if content is not None:
            note.content = content
        else:
            note.Contents = ""

        if priority_level is not None:
            note.priority_level = priority_level
        else:
            note.PriorityLevel = PriorityLevels.get_priority_levels(value=1)

        try:
            note.save()
            return note
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create note")

    def modify(self, content=None, priority_level=None):
        self.modification_date = datetime.now()

        if content is not None:
            self.content = content

        if priority_level is not None:
            self.priority_level = priority_level

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save note")

    @staticmethod
    def get_notes(
        note_id=None,
        creator=None,
        date_of_creation=None,
        date_of_modification=None,
        priority_level=None,
        title=None,
    ):
        try:
            all_notes = md.Notes.objects.all()

            if note_id is not None:
                all_notes.filter(note_id=note_id)

            if creator is not None:
                all_notes.filter(note_creator=creator)

            if title is not None:
                all_notes.filter(title=title)

            if date_of_creation is not None:
                all_notes.filter(creation_date=date_of_creation)

            if priority_level is not None:
                all_notes.filter(priority_level=priority_level)

            if date_of_modification is not None:
                all_notes.filter(modification_date=date_of_modification)

            return all_notes
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find such note")

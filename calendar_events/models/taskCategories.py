from datetime import timedelta
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import exceptions as e
from calendar_events.models.users import Users
from calendar_events.models.priorityLevels import PriorityLevels


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
    default_deadline = models.DurationField(null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create_task_category(
        user: Users,
        name: str,
        default_priority_level: PriorityLevels,
        default_acceptable_slide_time: timedelta,
        description: str = None,
        default_reminder_time: timedelta = None,
        default_localization: str = None,
        default_color: str = None,
        default_deadline: timedelta = None,
    ):
        task_category = TaskCategories()
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

        if default_deadline is not None:
            task_category.default_deadline = default_deadline

        try:
            task_category.save()
            return task_category
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create task category")

    @staticmethod
    def get_task_categories(
        task_category_id: int = None, user: Users = None, name: str = None
    ):
        if task_category_id is None and user is None and name is None:
            raise e.NoDataGiven("Need to specify task category")

        try:
            if task_category_id is not None:
                return TaskCategories.objects.get(task_category_id=task_category_id)
            elif user is not None:
                return TaskCategories.objects.get(task_category_creator=user)
            else:
                return TaskCategories.objects.get(name=name)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified task category")

    def modify(
        self,
        name: str = None,
        description: str = None,
        default_priority_level: PriorityLevels = None,
        default_acceptable_slide_time: timedelta = None,
        default_reminder_time: timedelta = None,
        default_localization: str = None,
        default_color: str = None,
        default_deadline: timedelta = None,
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
        if default_deadline is not None:
            self.default_deadline = default_deadline

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save task category")

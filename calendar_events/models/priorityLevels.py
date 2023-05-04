from datetime import timedelta
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import calendar_events.models as md
import exceptions as e
from calendar_events.models.users import Users


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
        user: Users,
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

        priority_level = PriorityLevels()
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
        pr_id: int = None, pr_name: str = None, user: Users = None, value=None
    ):
        if pr_id is None and pr_name is None and user is None and value is None:
            raise e.NoDataGiven("Need to specify some values")

        try:
            if pr_id is not None:
                return PriorityLevels.objects.get(priority_level_id=pr_id)
            elif pr_name is not None:
                return PriorityLevels.objects.get(name=pr_name)
            elif value is not None:
                return PriorityLevels.objects.get(priority_value=value)
            else:
                return PriorityLevels.objects.get(priority_level_creator=user.User)
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

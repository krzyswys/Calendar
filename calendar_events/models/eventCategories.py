from datetime import timedelta
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from calendar_events.models.priorityLevels import PriorityLevels
import exceptions as e
from calendar_events.models.users import Users


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
        user: Users,
        name: str,
        default_priority_level: PriorityLevels,
        default_duration_time: timedelta,
        description: str = None,
        default_localization: str = None,
        default_color: str = None,
        default_reminder_time: timedelta = None,
    ):
        event_category = EventCategories()
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
                return EventCategories.objects.get(event_categeory_id=cat_id)
            else:
                return EventCategories.objects.get(name=cat_name)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified event category")

    def modify(
        self,
        name: str = None,
        description: str = None,
        default_priority_level: PriorityLevels = None,
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

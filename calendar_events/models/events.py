from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import calendar_events.models as md
import exceptions as e
from calendar_events.models.eventCategories import EventCategories
from calendar_events.models.users import Users
from calendar_events.models.priorityLevels import PriorityLevels
from calendar_events.models.repeatPattern import RepeatPatterns


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
        user: Users,
        event_category: EventCategories,
        name: str,
        repeat_pattern: RepeatPatterns,
        first_occurrence: datetime,
        description: str = None,
        duration: timedelta = None,
        priority_level: PriorityLevels = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
    ):
        event = Events()
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
        event_category: EventCategories = None,
        user: Users = None,
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
                return Events.objects.get(event_id=event_id)
            elif event_name is not None:
                return Events.objects.get(name=event_name)
            else:
                all_rows = Events.objects.all()

                if event_category is not None:
                    all_rows = all_rows.filter(event_category=event_category)

                if user is not None:
                    all_rows = all_rows.filter(event_creator=user)

                return all_rows
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified event")

    def modify(
        self,
        event_category: EventCategories = None,
        name: str = None,
        description: str = None,
        duration: timedelta = None,
        repeat_pattern: RepeatPatterns = None,
        priority_level: PriorityLevels = None,
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
            start_date += relativedelta(
                years=repeat_pattern.years_interval,
                months=repeat_pattern.months_interval,
                weeks=repeat_pattern.weeks_interval,
                days=repeat_pattern.days_interval,
            )
            occurrence = EventOccurrences.create_event_occurrence(
                event=event, start_time=start_date
            )


class EventOccurrences(models.Model):
    event_occurrence_id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

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

    @staticmethod
    def create_event_occurrence(event: Events, start_time: datetime):
        event_occurrence = EventOccurrences()
        event_occurrence.event = event
        event_occurrence.start_time = start_time

        event_occurrence.event_creator = event.event_creator
        event_occurrence.event_category = event.event_category
        event_occurrence.priority_level = event.priority_level
        event_occurrence.repeat_pattern = event.repeat_pattern
        event_occurrence.name = event.name
        event_occurrence.description = event.description
        event_occurrence.reminder_time = event.reminder_time
        event_occurrence.localization = event.localization
        event_occurrence.duration = event.duration
        event_occurrence.creation_date = datetime.now()
        event_occurrence.color = event.color
        event_occurrence.first_occurrence = datetime.now()

        try:
            event_occurrence.save()
            return event_occurrence
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create event occurrence")

    @staticmethod
    def get_event_occurrences(
        id_event_occurrence: int = None,
        event: Events = None,
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
            all_occurrences = EventOccurrences.objects.all()
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

    def modify(
        self,
        event: Events = None,
        event_category: EventCategories = None,
        name: str = None,
        description: str = None,
        duration: timedelta = None,
        repeat_pattern: RepeatPatterns = None,
        priority_level: PriorityLevels = None,
        reminder_time: timedelta = None,
        localization: str = None,
        color: str = None,
    ):
        if event is not None:
            self.event = event
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
            raise e.EntityAlreadyExists("Cannot save event occurrence")

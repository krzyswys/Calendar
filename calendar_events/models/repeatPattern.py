from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import calendar_events.models as md
import exceptions as e
from calendar_events.models.users import Users


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
        user: Users,
        name: str,
        days_interval: int,
        weeks_interval: int,
        months_interval: int,
        years_interval: int,
        number_of_repetitions: int = 1,
    ):
        repeat_pattern = RepeatPatterns()
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
                return RepeatPatterns.objects.get(repeat_pattern_id=rp_id)
            else:
                return RepeatPatterns.objects.get(name=rp_name)
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

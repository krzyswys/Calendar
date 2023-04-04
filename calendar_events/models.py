from datetime import datetime
from django.db import models


class Users(models.Model):
    UserID = models.BigAutoField(primary_key=True)
    Login = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.Login


class PriorityLevels(models.Model):
    PriorityLevelID = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)
    Priority = models.IntegerField()
    Markdown = models.CharField(max_length=1)
    DefaultReminderTime = models.DurationField()

    def __str__(self):
        return self.Name


class EventCategories(models.Model):
    EventCategoryID = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    Name = models.CharField(max_length=60)
    Description = models.CharField(max_length=500)
    DefaultPriorityLevel = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    DefaultReminderTime = models.DurationField()
    DefaultLocalization = models.CharField(max_length=60)
    DefaultDurationTime = models.DurationField()
    DefaultColor = models.CharField(max_length=3)

    def __str__(self):
        return self.Name


class RepeatPatterns(models.Model):
    RepeatPatternID = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    DaysInterval = models.IntegerField()
    WeeksInterval = models.IntegerField()
    MonthsInterval = models.IntegerField()
    YearsInterval = models.IntegerField()
    Repetitions = models.IntegerField()


class Events(models.Model):
    EventID = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    EventCategory = models.ForeignKey(EventCategories, on_delete=models.CASCADE)
    PriorityLevel = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    RepeatPattern = models.ForeignKey(RepeatPatterns, on_delete=models.CASCADE)
    Name = models.CharField(max_length=60)
    Description = models.CharField(max_length=500)
    ReminderTime = models.DurationField()
    Localization = models.CharField(max_length=60)
    Duration = models.DurationField()
    CreationDate = models.DateTimeField(default=datetime.now)
    Color = models.CharField(max_length=3)
    #FirstOccurence

    def __str__(self):
        return self.Name


class EventOccurrences(models.Model):
    EventOccurrenceID = models.BigAutoField(primary_key=True)
    Event = models.ForeignKey(Events, on_delete=models.CASCADE)
    StartTime = models.DateTimeField()


class TaskCategories(models.Model):
    TaskCategoryID = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    Name = models.CharField(max_length=60)
    Description = models.CharField(max_length=500)
    DefaultPriorityLevel = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    DefaultReminderTime = models.DurationField()
    DefaultLocalization = models.CharField(max_length=60)
    DefaultColor = models.CharField(max_length=3)
    DefaultAcceptableSlideTime = models.DurationField()

    def __str__(self):
        return self.Name


class Tasks(models.Model):
    TaskID = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    TaskCategory = models.ForeignKey(TaskCategories, on_delete=models.CASCADE)
    PriorityLevel = models.ForeignKey(PriorityLevels, on_delete=models.CASCADE)
    RepeatPattern = models.ForeignKey(RepeatPatterns, on_delete=models.CASCADE)
    Name = models.CharField(max_length=60)
    Description = models.CharField(max_length=500)
    ReminderTime = models.DurationField()
    Localization = models.CharField(max_length=60)
    CreationDate = models.DateTimeField(default=datetime.now)
    Color = models.CharField(max_length=3)
    ExpectedCompletionDate = models.DateTimeField()
    Deadline = models.DateTimeField()
    AcceptableSlideTime = models.DurationField()

    class StatusOptions(models.IntegerChoices):
        (0, 'Not finished'),
        (1, 'Finished')

    Status = models.IntegerField(choices=StatusOptions)

    def __str__(self):
        return self.Name


class TaskOccurrences(models.Model):
    TaskOccurrenceID = models.BigAutoField(primary_key=True)
    Task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    StartTime = models.DateTimeField()


from rest_framework import serializers

from calendar_events.models.events import Events, EventOccurrences
from calendar_events.models.eventCategories import EventCategories
from calendar_events.models.tasks import Tasks, TaskOccurrences
from calendar_events.models.taskCategories import TaskCategories
from calendar_events.models.notes import Notes
from calendar_events.models.priorityLevels import PriorityLevels
from calendar_events.models.repeatPattern import RepeatPatterns
from calendar_events.models.users import Users

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"


class EventOccurrencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOccurrences
        fields = "__all__"


class EventCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategories
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"


class TaskOccurrencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOccurrences
        fields = "__all__"


class TaskCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategories
        fields = "__all__"


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = "__all__"


class PriorityLevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityLevels
        fields = "__all__"


class RepeatPatternsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepeatPatterns
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"



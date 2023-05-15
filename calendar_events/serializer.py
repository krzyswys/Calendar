from rest_framework import serializers

from calendar_events.models.events import Events


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"

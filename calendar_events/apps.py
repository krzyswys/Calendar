from django.apps import AppConfig


class CalendarEventsConfig(AppConfig):
    name = "calendar_events"

    def ready(self):
        from .models import Users, PriorityLevels
        from .generate_sample_data import generate_data

        generate_data()

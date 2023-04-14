from django.apps import AppConfig


class CalendarEventsConfig(AppConfig):
<<<<<<< HEAD
    name = 'calendar_events'
=======
    name = "calendar_events"

    def ready(self):
        from .models import Users, PriorityLevels
        from .generate_sample_data import generate_data

        generate_data()
>>>>>>> 849d243 (added statictic functions for events and tasks, html view for individual tables, functions applying patterns, fake data generator on server run file)

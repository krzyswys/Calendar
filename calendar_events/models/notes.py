from datetime import datetime
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import calendar_events.models as md
import exceptions as e
from calendar_events.models.users import Users
from calendar_events.models.priorityLevels import PriorityLevels


class Notes(models.Model):
    note_id = models.BigAutoField(primary_key=True)
    note_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=4000)
    content = models.CharField(max_length=4000)
    creation_date = models.DateTimeField(default=datetime.now)
    modification_date = models.DateTimeField(default=datetime.now)
    priority_level = models.ForeignKey(
        PriorityLevels, on_delete=models.CASCADE, null=True
    )

    @staticmethod
    def create_note(creator: Users, title, content=None, priority_level=None):
        note = Notes()
        note.note_creator = creator
        note.title = title

        if content is not None:
            note.content = content
        else:
            note.Contents = ""

        if priority_level is not None:
            note.priority_level = priority_level
        else:
            note.PriorityLevel = PriorityLevels.get_priority_levels(value=1)

        try:
            note.save()
            return note
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot create note")

    def modify(self, content=None, priority_level=None):
        self.modification_date = datetime.now()

        if content is not None:
            self.content = content

        if priority_level is not None:
            self.priority_level = priority_level

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("Cannot save note")

    @staticmethod
    def get_notes(
        note_id=None,
        creator=None,
        date_of_creation=None,
        date_of_modification=None,
        priority_level=None,
        title=None,
    ):
        try:
            all_notes = Notes.objects.all()

            if note_id is not None:
                all_notes.filter(note_id=note_id)

            if creator is not None:
                all_notes.filter(note_creator=creator)

            if title is not None:
                all_notes.filter(title=title)

            if date_of_creation is not None:
                all_notes.filter(creation_date=date_of_creation)

            if priority_level is not None:
                all_notes.filter(priority_level=priority_level)

            if date_of_modification is not None:
                all_notes.filter(modification_date=date_of_modification)

            return all_notes
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find such note")

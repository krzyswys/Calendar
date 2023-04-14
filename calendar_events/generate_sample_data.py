import random
from faker import Faker
from calendar_events.models import *
from datetime import timedelta

# user is set to default as 'some_user'


def generate_user():
    user = Users.create_user(login="some_user")
    user.save()


def generate_prioity_levels(n=5):
    for i in range(n):
        minutes = random.randint(0, 60)
        hours = random.randint(0, 24)
        td = timedelta(hours=hours, minutes=minutes)
        name = "Priority level: " + str(i)
        plevel = PriorityLevels.create_priority_level(
            user=Users.get_user(login="some_user"),
            name=name,
            priority=i,
            default_reminder_time=td,
        )
        # plevel.save()


def generate_event_categories(n=5):
    fake = Faker()
    for i in range(n):
        event_name = (
            fake.color_name()
            + " "
            + fake.random_element(elements=("Party", "Event", "Lecture", "Class"))
        )
        minutes = random.randint(0, 60)
        hours = random.randint(0, 24)
        td1 = timedelta(hours=hours, minutes=minutes)
        minutes = random.randint(0, 60)
        hours = random.randint(0, 24)
        td2 = timedelta(hours=hours, minutes=minutes)
        name = "Priority level: " + str(i)
        pr = PriorityLevels.objects.all()
        random_pr = random.choice(pr)

        description = random.choice([None, fake.paragraph()])
        localization = random.choice([None, fake.address()])
        color = random.choice([None, fake.hex_color()])
        ev = EventCategories.create_event_category(
            user=Users.get_user(login="some_user"),
            name=event_name,
            default_priority_level=random_pr,
            default_duration_time=td1,
            default_reminder_time=td2,
            description=description,
            default_localization=localization,
            default_color=color,
        )
        # ev.save()


def generate_repeat_patterns(n=5):
    fake = Faker()
    for i in range(n):
        days = random.randint(1, 7)
        weeks = random.randint(1, 4)
        months = random.randint(1, 12)
        year = random.randint(1, 2)
        rep = random.randint(1, 10)
        pattern_name = (
            "D" + str(days) + "W" + str(weeks) + "M" + str(months) + "Y" + str(year)
        )
        repeat_pattern = RepeatPatterns.create_repeat_pattern(
            user=Users.get_user(login="some_user"),
            name=pattern_name,
            days_interval=days,
            weeks_interval=weeks,
            months_interval=months,
            years_interval=year,
            number_of_repetitions=rep,
        )
        # repeat_pattern.save()


def generate_events(n=5):
    fake = Faker()
    for i in range(n):
        ec = EventCategories.objects.all()
        random_ec = random.choice(ec)
        name = random_ec.name + " -> event"
        rp = RepeatPatterns.objects.all()
        random_rp = random.choice(rp)
        pr = PriorityLevels.objects.all()
        random_pr = random.choice(pr)
        description = random.choice([None, fake.paragraph()])
        duration = random.choice(
            [None, timedelta(minutes=fake.random_int(min=15, max=240))]
        )
        reminder_time = timedelta(minutes=fake.random_int(min=5, max=60))
        localization = random.choice([None, fake.address()])
        color = random.choice([None, fake.hex_color()])
        first_occurance = fake.date_time_between(start_date="-1y", end_date="now")
        event = Events.create_event(
            user=Users.get_user(login="some_user"),
            event_category=random_ec,
            name=name,
            repeat_pattern=random_rp,
            first_occurrence=first_occurance,
            description=description,
            duration=duration,
            priority_level=random_pr,
            reminder_time=reminder_time,
            localization=localization,
            color=color,
        )
        event.apply_event_pattern_for(event)
        # event.save()


def generate_task_categories(n=5):
    fake = Faker()
    for i in range(n):
        task_name = (
            fake.color_name()
            + " "
            + fake.random_element(elements=("Excercise", "Shop", "Work", "Home"))
        )
        pr = PriorityLevels.objects.all()
        random_pr = random.choice(pr)
        description = random.choice([None, fake.paragraph()])
        duration = random.choice(
            [None, timedelta(minutes=fake.random_int(min=15, max=240))]
        )
        reminder_time = timedelta(minutes=fake.random_int(min=5, max=60))
        localization = random.choice([None, fake.address()])
        color = random.choice([None, fake.hex_color()])
        slide_time = timedelta(
            weeks=fake.random_int(min=1, max=52),
            days=fake.random_int(min=1, max=30),
            hours=fake.random_int(min=1, max=24),
            minutes=fake.random_int(min=1, max=60),
        )
        rp = RepeatPatterns.objects.all()
        random_rp = random.choice([None, random.choice(rp)])

        ev = TaskCategories.create_task_category(
            user=Users.get_user(login="some_user"),
            name=task_name,
            default_priority_level=random_pr,
            default_acceptable_slide_time=slide_time,
            description=description,
            default_reminder_time=reminder_time,
            default_localization=localization,
            default_color=color,
        )
        # ev.save()


def generate_tasks(n=5):
    fake = Faker()
    for i in range(n):
        tc = TaskCategories.objects.all()
        random_tc = random.choice(tc)
        rp = RepeatPatterns.objects.all()
        random_rp = random.choice(rp)
        pr = PriorityLevels.objects.all()
        random_pr = random.choice(pr)
        description = random.choice([None, fake.paragraph()])
        reminder_time = timedelta(minutes=fake.random_int(min=5, max=60))
        localization = random.choice([None, fake.address()])
        color = random.choice([None, fake.hex_color()])
        slide_time = timedelta(
            weeks=fake.random_int(min=1, max=52),
            days=fake.random_int(min=1, max=30),
            hours=fake.random_int(min=1, max=24),
            minutes=fake.random_int(min=1, max=60),
        )
        first_occurance = fake.date_time_between(start_date="-1y", end_date="now")
        now = datetime.now()
        expected_completion_data = fake.date_between_dates(
            date_start=now, date_end=now + timedelta(days=30)
        )
        deadline = fake.date_between_dates(
            date_start=now, date_end=now + timedelta(days=30)
        )
        t = Tasks.create_task(
            user=Users.get_user(login="some_user"),
            task_category=random_tc,
            priority_level=random_pr,
            repeat_pattern=random_rp,
            name=random_tc.name + "task",
            expected_completion_date=expected_completion_data,
            first_occurrence=first_occurance,
            description=description,
            reminder_time=reminder_time,
            localization=localization,
            color=color,
            deadline=deadline,
            acceptable_slide_time=slide_time,
        )
        # t.save()
        t.apply_task_pattern_for(t)


def generate_notes(n=5):
    fake = Faker()
    for i in range(n):
        content = fake.text()
        pr = PriorityLevels.objects.all()
        random_pr = random.choice(pr)
        pr = random.choice([None, random_pr])
        title = fake.paragraph(nb_sentences=1)
        note = Notes.create_note(
            creator=Users.get_user(login="some_user"),
            Title=title,
            contents=content,
            prioriy_level=pr,
        )
        # note.save()


def load_data():
    Users.objects.all().delete()
    PriorityLevels.objects.all().delete()
    EventCategories.objects.all().delete()
    RepeatPatterns.objects.all().delete()
    Events.objects.all().delete()
    TaskCategories.objects.all().delete()
    Tasks.objects.all().delete()
    Notes.objects.all().delete()
    n = 3
    generate_user()
    generate_prioity_levels(n)
    generate_event_categories(n)
    generate_repeat_patterns(n)
    generate_events(n)
    generate_task_categories(n)
    generate_tasks(n)
    generate_notes()


def generate_data():
    # load_data();
    pass

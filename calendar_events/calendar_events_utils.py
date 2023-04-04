import datetime
import calendar_events.models as md


def create_user(login: str):
    if login is not None:
        user = md.Users()
        user.Login = login
        user.save()
    else:
        raise Exception("Login cannot be None")


def get_user(user_id: int = None, login: str = None):
    if user_id is not None:
        return md.Users.objects.get(UserID=user_id)
    elif login is not None:
        return md.Users.objects.get(Login=login)
    else:
        raise Exception("Not specified user")


def modify_user(user: md.Users, new_login: str):
    if new_login is None:
        raise Exception("New login cannot be None")

    user.Login = new_login
    user.save()


def delete_user(user: md.Users):
    user.delete()


def create_priority_level(
    name: str,
    priority: int,
    markdown: str,
    default_reminder_time: datetime.timedelta,
    user: md.Users,
):
    priority_level = md.PriorityLevels()
    priority_level.Creator = user
    priority_level.Name = name
    priority_level.Priority = priority
    priority_level.Markdown = markdown
    priority_level.DefaultReminderTime = default_reminder_time
    priority_level.save()


def get_priority_level(pr_id: int = None, pr_name: str = None, user: md.Users = None):
    if pr_id is not None:
        return md.PriorityLevels.objects.get(PriorityLevelID=pr_id)
    elif pr_name is not None:
        return md.PriorityLevels.objects.get(Name=pr_name)
    elif user is not None:
        return md.PriorityLevels.objects.get(Creator=user.User)
    else:
        raise Exception("Not specified priority level")


def modify_priority_level(
    priority_level: md.PriorityLevels,
    name: str = None,
    priority: int = None,
    markdown: str = None,
    default_reminder_time: datetime.timedelta = None,
):
    if name is not None:
        priority_level.Name = name

    if priority is not None:
        priority_level.Priority = priority

    if markdown is not None:
        priority_level.Markdown = markdown

    if default_reminder_time is not None:
        priority_level.DefaultReminderTime = default_reminder_time

    priority_level.save()


def delete_priority_level(priority_level: md.PriorityLevels):
    priority_level.delete()


def create_event_category(
    user: md.Users,
    name: str,
    description: str,
    default_priority_level: md.PriorityLevels,
    default_localization: str,
    default_duration_time: datetime.timedelta,
    default_color: str,
    default_reminder_time: datetime.timedelta = None,
):
    event_category = md.EventCategories()
    event_category.Creator = user
    event_category.Name = name
    event_category.Description = description
    event_category.DefaultPriorityLevel = default_priority_level

    if default_reminder_time is not None:
        event_category.DefaultReminderTime = default_reminder_time
    else:
        event_category.DefaultReminderTime = default_priority_level.DefaultReminderTime

    event_category.DefaultLocalization = default_localization
    event_category.DefaultDurationTime = default_duration_time
    event_category.DefaultColor = default_color

    event_category.save()


def get_event_category(cat_id: int = None, cat_name: str = None):
    if cat_id is not None:
        return md.EventCategories.objects.get(EventCategoryID=cat_id)
    elif cat_name is not None:
        return md.EventCategories.objects.get(Name=cat_name)
    else:
        raise Exception("Not specified event category")


def modify_event_category(
    event_category: md.EventCategories,
    name: str = None,
    description: str = None,
    default_priority_level: md.PriorityLevels = None,
    default_localization: str = None,
    default_duration_time: datetime.timedelta = None,
    default_color: str = None,
    default_reminder_time: datetime.timedelta = None,
):
    if name is not None:
        event_category.Name = name

    if description is not None:
        event_category.Description = description

    if default_priority_level is not None:
        event_category.DefaultPriorityLevel = default_priority_level

    if default_localization is not None:
        event_category.DefaultLocalization = default_localization

    if default_duration_time is not None:
        event_category.DefaultDurationTime = default_duration_time

    if default_color is not None:
        event_category.DefaultColor = default_color

    if default_reminder_time is not None:
        event_category.DefaultReminderTime = default_reminder_time

    event_category.save()


def delete_event_category(event_category: md.EventCategories):
    event_category.delete()


def create_event(
    user: md.Users,
    event_category: md.EventCategories,
    name: str,
    description: str,
    duration: datetime.timedelta,
    repeat_pattern: md.RepeatPatterns,
    priority_level: md.PriorityLevels = None,
    reminder_time: datetime.timedelta = None,
    localization: str = None,
    color: str = None,
):
    event = md.Events()
    event.Creator = user
    event.EventCategory = event_category
    event.RepeatPattern = repeat_pattern
    event.Name = name
    event.Description = description
    event.Duration = duration

    if priority_level is None:
        event.PriorityLevel = event_category.DefaultPriorityLevel
    else:
        event.PriorityLevel = priority_level

    if reminder_time is None:
        event.ReminderTime = event_category.DefaultReminderTime
    else:
        event.ReminderTime = reminder_time

    if localization is None:
        event.Localization = event_category.DefaultLocalization
    else:
        event.Localization = localization

    if color is None:
        event.Color = event_category.DefaultColor
    else:
        event.Color = color

    event.save()


def get_event(event_id: int = None, event_name: str = None):
    if event_id is not None:
        return md.Events.objects.get(EventID=event_id)
    elif event_name is not None:
        return md.Events.objects.get(Name=event_name)
    else:
        raise Exception("Not specified event")


def modify_event(
    event: md.Events,
    event_category: md.EventCategories = None,
    name: str = None,
    description: str = None,
    duration: datetime.timedelta = None,
    repeat_pattern: md.RepeatPatterns = None,
    priority_level: md.PriorityLevels = None,
    reminder_time: datetime.timedelta = None,
    localization: str = None,
    color: str = None,
):
    if event_category is not None:
        event.EventCategory = event_category

    if name is not None:
        event.Name = name

    if description is not None:
        event.Description = description

    if duration is not None:
        event.Duration = duration

    if repeat_pattern is not None:
        event.RepeatPattern = repeat_pattern

    if priority_level is not None:
        event.PriorityLevel = priority_level

    if reminder_time is not None:
        event.ReminderTime = reminder_time

    if localization is not None:
        event.Localization = localization

    if color is not None:
        event.Color = color

    event.save()


def delete_event(event: md.Events):
    event.delete()

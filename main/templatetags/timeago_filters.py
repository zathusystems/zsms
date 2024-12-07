# your_app/templatetags/custom_filters.py
import datetime
from django import template
from django.utils.timezone import now

register = template.Library()

@register.filter
def timeago(value):
    if not isinstance(value, datetime.datetime):
        return value

    now_time = now()
    delta = now_time - value

    # Calculate different time intervals
    seconds = delta.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7
    months = days / 30
    years = days / 365

    # Customize output
    if seconds < 60:
        return f"{int(seconds)}s"
    elif minutes < 60:
        return f"{int(minutes)}m"
    elif hours < 24:
        return f"{int(hours)}h"
    elif days < 7:
        return f"{int(days)}d"
    elif weeks < 4:
        return f"{int(weeks)}w"
    elif months < 12:
        return f"{int(months)}mo"
    else:
        return f"{int(years)}y"



# your_app/templatetags/custom_filters.py

from django import template
from django.utils import timezone
import datetime

# myapp/templatetags/custom_filters.py

from django import template
from datetime import datetime, timedelta
from django.utils.timezone import now

register = template.Library()

@register.filter
def ticket_list_date_format(value):
    if not isinstance(value, datetime.datetime):
        return value

    today = timezone.now().date()
    date = value.date()

    def format_hour(value):
        hour = value.strftime("%I")
        return hour.lstrip("0")

    if date == today:
        return f"Today @ {format_hour(value)}:{value.strftime('%M %p')}"

    day = value.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    return f"{value.strftime('%a, %b')} {day}{suffix} @ {format_hour(value)}:{value.strftime('%M %p')}"

@register.filter(name='ticket_detail_date_format')
def ticket_detail_date_format(value):
    if not isinstance(value, datetime.datetime):
        return value

    def format_hour(value):
        hour = value.strftime("%I")
        return hour.lstrip("0")

    day = value.day

    return f"{value.strftime('%A, %B')} {day} at {format_hour(value)}:{value.strftime('%M %p').lower()}"

register = template.Library()

@register.filter
def is_within_24_hours(date_time):
    """
    Returns True if the given datetime is within the last 24 hours.
    """
    if not date_time:
        return False
    current_time = now()
    return date_time >= current_time - timedelta(hours=24)
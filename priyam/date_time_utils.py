"""
Date and time utilities for common operations.
"""

from datetime import datetime, timedelta
import pytz
from dateutil import rrule
from dateutil.relativedelta import relativedelta

def convert_timezone(dt, from_tz, to_tz):
    """
    Convert a datetime from one timezone to another.
    
    Args:
        dt (datetime): The datetime to convert.
        from_tz (str): The source timezone (e.g., 'UTC', 'US/Eastern').
        to_tz (str): The target timezone (e.g., 'UTC', 'US/Eastern').
        
    Returns:
        datetime: The converted datetime.
        
    Example:
        >>> dt = datetime(2023, 1, 1, 12, 0, 0)
        >>> convert_timezone(dt, 'UTC', 'US/Eastern')
        datetime.datetime(2023, 1, 1, 7, 0, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
    """
    from_zone = pytz.timezone(from_tz)
    to_zone = pytz.timezone(to_tz)
    
    if dt.tzinfo is None:
        dt = from_zone.localize(dt)
    
    return dt.astimezone(to_zone)

def countdown_timer(end_time):
    """
    Calculate the time remaining until a specified end time.
    
    Args:
        end_time (datetime): The end time to count down to.
        
    Returns:
        dict: A dictionary with days, hours, minutes, and seconds remaining.
        
    Example:
        >>> end_time = datetime.now() + timedelta(days=1, hours=2, minutes=30)
        >>> countdown_timer(end_time)
        {'days': 1, 'hours': 2, 'minutes': 30, 'seconds': 0}
    """
    now = datetime.now(pytz.UTC) if end_time.tzinfo else datetime.now()
    time_remaining = end_time - now
    
    if time_remaining.total_seconds() < 0:
        return {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
    
    days = time_remaining.days
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

def working_days_calculator(start_date, end_date, holidays=None):
    """
    Calculate the number of working days between two dates.
    
    Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.
        holidays (list): List of holiday dates to exclude.
        
    Returns:
        int: The number of working days.
        
    Example:
        >>> start = datetime(2023, 1, 1)
        >>> end = datetime(2023, 1, 10)
        >>> working_days_calculator(start, end)
        6
    """
    if holidays is None:
        holidays = []
    
    # Create a rule for weekdays (Monday to Friday)
    rule = rrule.rrule(
        rrule.DAILY,
        byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR],
        dtstart=start_date,
        until=end_date
    )
    
    # Count working days excluding holidays
    working_days = 0
    for dt in rule:
        if dt.date() not in holidays:
            working_days += 1
    
    return working_days
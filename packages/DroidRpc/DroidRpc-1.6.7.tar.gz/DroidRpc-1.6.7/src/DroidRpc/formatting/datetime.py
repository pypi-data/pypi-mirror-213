# Contains functions used to manipulate dates and times.
from functools import cache
from datetime import datetime
import re

def string_to_date(date_string):
    """Convert a string to a datetime object."""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}, expected format: YYYY-MM-DD")

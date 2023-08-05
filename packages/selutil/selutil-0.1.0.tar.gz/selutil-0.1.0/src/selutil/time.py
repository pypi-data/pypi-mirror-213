"""Commonly used time functionality."""
from datetime import datetime, timezone
import sqlite3
from typing import List, Union


def get_timestamp(timestamp: Union[datetime, None] = None) -> str:
    """Return a timestamp conformant with ISO 8601.

    Args:
        timestamp: The datetime object of the time to return the formatted time
                   stamp.  If not supplied, the current time in UTC is used.

    Returns:
        A string containing the time in YYYY-MM-DDTHH:MM:SS.ms+ZZ:ZZ.  If some
        portions are not in the input datetime option, they will be left off.
    """
    return datetime.isoformat(timestamp or datetime.now(timezone.utc))

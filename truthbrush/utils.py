from datetime import timezone
from dateutil import parser as date_parse


"""Utility Functions"""


def as_datetime(date_str):
    """Datetime formatter function. Ensures timezone is UTC.

    Params :
        date_str (str) : Date string, like '2024-07-14 14:50:31.628257+00:00'
                        formatted like the ones returned by the API.

    """
    return date_parse.parse(date_str).replace(tzinfo=timezone.utc)

"""
Julian day conversion utilities.

Julian days are a continuous count of days since January 1, 4713 BC (proleptic
Julian calendar). They're used extensively in astronomy to avoid calendar
complications. JD 0 starts at noon (12:00 UTC), not midnight.

This is simple astronomy stuff. No magic, no bullshit.
"""

import datetime
import math
from typing import Union


# Gregorian calendar reform date: October 15, 1582
# JD 2299160.5 corresponds to midnight of that date
GREGORIAN_EPOCH = 2299160


def jd_to_datetime(jd: Union[int, float]) -> datetime.datetime:
    """
    Convert Julian day number to UTC datetime.

    Uses the standard astronomical algorithm with Gregorian calendar correction.

    Args:
        jd: Julian day number (can be fractional for sub-day precision)

    Returns:
        datetime.datetime: UTC datetime corresponding to the Julian day

    Example:
        >>> jd_to_datetime(2451545.0)  # J2000 epoch
        datetime.datetime(2000, 1, 1, 12, 0)
    """
    if not isinstance(jd, (int, float)):
        raise TypeError(f"Julian day must be int or float, not {type(jd).__name__}")

    # Julian days start at noon, so we shift by 0.5 to get midnight-based days
    jd = jd + 0.5
    jd_frac, jd_int = math.modf(jd)
    jd_int = int(jd_int)

    # Gregorian calendar correction for dates after October 15, 1582
    if jd_int > GREGORIAN_EPOCH:
        alpha = int((jd_int - 1867216.25) / 36524.25)
        b = jd_int + 1 + alpha - int(alpha / 4)
    else:
        b = jd_int

    c = b + 1524
    d = int((c - 122.1) / 365.25)
    e = int(365.25 * d)
    g = int((c - e) / 30.6001)

    # Calculate day with fractional part
    day = c - e + jd_frac - int(30.6001 * g)

    # Month calculation
    month = g - 1 if g < 13.5 else g - 13
    month = int(month)

    # Year calculation
    year = d - 4716 if month > 2.5 else d - 4715
    year = int(year)

    # Split day into integer day and fractional part for time
    day_frac, day_int = math.modf(day)
    day_int = int(day_int)

    # Convert fractional day to hours/minutes/seconds/microseconds
    hours_dec = day_frac * 24.0
    hours_frac, hours = math.modf(hours_dec)

    minutes_dec = hours_frac * 60.0
    minutes_frac, minutes = math.modf(minutes_dec)

    seconds_dec = minutes_frac * 60.0
    seconds_frac, seconds = math.modf(seconds_dec)

    microseconds = int(seconds_frac * 1e6)

    return datetime.datetime(
        year, month, day_int,
        int(hours), int(minutes), int(seconds), microseconds
    )


def datetime_to_jd(dt: datetime.datetime) -> float:
    """
    Convert UTC datetime to Julian day number.

    This is the inverse of jd_to_datetime(). Naive datetimes are treated as UTC.

    Args:
        dt: datetime to convert (assumed UTC if naive)

    Returns:
        float: Julian day number with fractional day precision

    Example:
        >>> datetime_to_jd(datetime.datetime(2000, 1, 1, 12, 0))
        2451545.0
    """
    if not isinstance(dt, datetime.datetime):
        raise TypeError(f"Expected datetime.datetime, not {type(dt).__name__}")

    year = dt.year
    month = dt.month
    day = dt.day

    # Month/year adjustment for the algorithm
    if month <= 2:
        year -= 1
        month += 12

    # Gregorian calendar correction
    if dt >= datetime.datetime(1582, 10, 15):
        a = int(year / 100)
        b = 2 - a + int(a / 4)
    else:
        b = 0

    # Standard Julian day calculation
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5

    # Add fractional day from time components
    hours = dt.hour
    minutes = dt.minute
    seconds = dt.second
    microseconds = dt.microsecond

    fractional_day = (hours + minutes / 60.0 + seconds / 3600.0 +
                     microseconds / 3600.0 / 1e6) / 24.0

    return jd + fractional_day


# Alias for backward compatibility
juliandate_to_datetime = jd_to_datetime

from datetime import datetime
from convert_julian_day import juliandate_to_datetime


def test_j2000():
    dt = juliandate_to_datetime(2451545)
    assert dt == datetime(2000, 1, 1, 12, 0)

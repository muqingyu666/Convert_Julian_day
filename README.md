# Julian Day Converter

Simple, no-bullshit conversion between Julian day numbers and UTC datetimes.

## What is a Julian Day?

Julian days are a continuous count of days since January 1, 4713 BC (proleptic Julian calendar). Astronomers use them to avoid calendar math headaches. JD 0 starts at **noon UTC**, not midnight.

**Example**: JD 2451545.0 = January 1, 2000, 12:00:00 UTC (J2000 epoch)

## Installation

```bash
pip install -e .
```

## Usage

### Command Line

**Convert JD to datetime:**
```bash
python -m convert_julian_day.cli 2451545
# Output: 2000-01-01T12:00:00
```

**Convert datetime to JD (reverse):**
```bash
python -m convert_julian_day.cli -r 2000-01-01
# Output: 2451544.500000

python -m convert_julian_day.cli -r "2000-01-01 12:00:00"
# Output: 2451545.000000
```

### Python API

```python
from convert_julian_day import jd_to_datetime, datetime_to_jd
import datetime

# JD -> datetime
dt = jd_to_datetime(2451545.0)
print(dt)  # 2000-01-01 12:00:00

# datetime -> JD
jd = datetime_to_jd(datetime.datetime(2000, 1, 1, 12, 0, 0))
print(jd)  # 2451545.0

# Fractional days work
dt = jd_to_datetime(2451545.25)  # 6 hours after noon
print(dt)  # 2000-01-01 18:00:00
```

### Backward Compatibility

The old `juliandate_to_datetime()` function still works:

```python
from convert_julian_day import juliandate_to_datetime

dt = juliandate_to_datetime(2451545)
```

## Testing

```bash
pip install pytest
pytest
```

## Algorithm

Uses the standard astronomical Julian date algorithm with Gregorian calendar correction for dates after October 15, 1582. No external dependencies - just Python stdlib.

## License

Do whatever you want with it. It's a calendar conversion, not rocket science.

## Notes

- Fractional Julian days give you sub-day precision (hours/minutes/seconds/microseconds)
- Naive datetimes are treated as UTC - if you pass timezone-aware datetimes, they're ignored
- The Gregorian calendar reform happened October 15, 1582. Dates before that use Julian calendar rules.
- Round-trip conversions maintain microsecond precision

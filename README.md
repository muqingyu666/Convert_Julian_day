# Convert Julian Day

Utilities for converting Julian day numbers to standard UTC datetimes.

## Usage

Install the package in editable mode (optional)::

    pip install -e .

Convert a Julian day from the command line:

```bash
python -m convert_julian_day.cli 2451545
```

Or use the API:

```python
from convert_julian_day import juliandate_to_datetime

print(juliandate_to_datetime(2451545))
```

The example above prints `2000-01-01 12:00:00`.

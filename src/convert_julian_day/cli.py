"""Command line interface for converting Julian days to UTC datetimes."""

import argparse
from .julian_day import juliandate_to_datetime


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Julian day to UTC datetime")
    parser.add_argument("julian_day", type=int, help="Julian day number")
    args = parser.parse_args()
    dt = juliandate_to_datetime(args.julian_day)
    print(dt.isoformat())


if __name__ == "__main__":
    main()

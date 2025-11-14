"""Command line interface for Julian day conversions."""

import argparse
import sys
import datetime
from .julian_day import jd_to_datetime, datetime_to_jd


def main() -> None:
    """Run the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert between Julian day numbers and UTC datetimes",
        epilog="""
Examples:
  %(prog)s 2451545           # Convert JD to datetime
  %(prog)s -r 2000-01-01     # Convert datetime to JD
  %(prog)s -r "2000-01-01 12:00:00"  # With time
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "value",
        help="Julian day number (e.g., 2451545) or datetime string (with -r)"
    )

    parser.add_argument(
        "-r", "--reverse",
        action="store_true",
        help="Convert datetime to Julian day (reverse conversion)"
    )

    args = parser.parse_args()

    try:
        if args.reverse:
            # Parse datetime string
            dt_str = args.value
            # Try ISO format first, then date-only format
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                try:
                    dt = datetime.datetime.strptime(dt_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                print(f"Error: Invalid datetime format '{dt_str}'", file=sys.stderr)
                print("Expected: YYYY-MM-DD or 'YYYY-MM-DD HH:MM:SS'", file=sys.stderr)
                sys.exit(1)

            jd = datetime_to_jd(dt)
            print(f"{jd:.6f}")
        else:
            # Convert JD to datetime
            try:
                jd = float(args.value)
            except ValueError:
                print(f"Error: Invalid Julian day '{args.value}'", file=sys.stderr)
                print("Expected: numeric value (e.g., 2451545 or 2451545.5)", file=sys.stderr)
                sys.exit(1)

            dt = jd_to_datetime(jd)
            print(dt.isoformat())

    except (TypeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

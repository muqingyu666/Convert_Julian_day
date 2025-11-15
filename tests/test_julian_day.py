"""Tests for Julian day conversion functions."""

import datetime
import pytest
from convert_julian_day import jd_to_datetime, datetime_to_jd, juliandate_to_datetime


class TestJDToDatetime:
    """Test Julian day to datetime conversion."""

    def test_j2000_epoch(self):
        """J2000 epoch: 2000-01-01 12:00:00 UTC = JD 2451545.0"""
        dt = jd_to_datetime(2451545.0)
        assert dt == datetime.datetime(2000, 1, 1, 12, 0, 0)

    def test_unix_epoch(self):
        """Unix epoch: 1970-01-01 00:00:00 UTC = JD 2440587.5"""
        dt = jd_to_datetime(2440587.5)
        assert dt == datetime.datetime(1970, 1, 1, 0, 0, 0)

    def test_fractional_day(self):
        """Test fractional Julian day (sub-day precision)."""
        # JD 2451545.25 = 2000-01-01 18:00:00 (6 hours after noon)
        dt = jd_to_datetime(2451545.25)
        assert dt == datetime.datetime(2000, 1, 1, 18, 0, 0)

    def test_pre_gregorian(self):
        """Test date before Gregorian calendar reform (Oct 15, 1582)."""
        # Just verify it doesn't crash
        dt = jd_to_datetime(2299160)  # ~1582-10-15
        assert isinstance(dt, datetime.datetime)

    def test_integer_input(self):
        """Test that integer input works (not just float)."""
        dt = jd_to_datetime(2451545)
        assert dt == datetime.datetime(2000, 1, 1, 12, 0, 0)

    def test_microsecond_precision(self):
        """Test microsecond precision in time."""
        # Add a tiny fractional component
        dt = jd_to_datetime(2451545.0000001)
        assert dt.microsecond > 0

    def test_backward_compatibility_alias(self):
        """Test that juliandate_to_datetime still works."""
        dt1 = jd_to_datetime(2451545)
        dt2 = juliandate_to_datetime(2451545)
        assert dt1 == dt2


class TestDatetimeToJD:
    """Test datetime to Julian day conversion."""

    def test_j2000_epoch(self):
        """J2000 epoch: 2000-01-01 12:00:00 UTC = JD 2451545.0"""
        dt = datetime.datetime(2000, 1, 1, 12, 0, 0)
        jd = datetime_to_jd(dt)
        assert abs(jd - 2451545.0) < 1e-6

    def test_unix_epoch(self):
        """Unix epoch: 1970-01-01 00:00:00 UTC = JD 2440587.5"""
        dt = datetime.datetime(1970, 1, 1, 0, 0, 0)
        jd = datetime_to_jd(dt)
        assert abs(jd - 2440587.5) < 1e-6

    def test_midnight(self):
        """Test midnight (00:00:00) correctly adds 0.5 to base JD."""
        dt = datetime.datetime(2000, 1, 1, 0, 0, 0)
        jd = datetime_to_jd(dt)
        # Noon is .0, so midnight is -0.5 from that = 2451544.5
        assert abs(jd - 2451544.5) < 1e-6

    def test_with_time_components(self):
        """Test datetime with hours, minutes, seconds."""
        dt = datetime.datetime(2000, 1, 1, 18, 30, 45, 123456)
        jd = datetime_to_jd(dt)
        # Should have fractional component
        assert jd != int(jd)

    def test_pre_gregorian(self):
        """Test date before Gregorian calendar reform."""
        dt = datetime.datetime(1582, 10, 4)  # Before reform
        jd = datetime_to_jd(dt)
        assert isinstance(jd, float)


class TestRoundTrip:
    """Test round-trip conversions (JD -> datetime -> JD and vice versa)."""

    def test_jd_roundtrip_j2000(self):
        """JD -> datetime -> JD should return original value."""
        original_jd = 2451545.0
        dt = jd_to_datetime(original_jd)
        result_jd = datetime_to_jd(dt)
        assert abs(result_jd - original_jd) < 1e-6

    def test_jd_roundtrip_fractional(self):
        """Round-trip with fractional JD."""
        original_jd = 2451545.75
        dt = jd_to_datetime(original_jd)
        result_jd = datetime_to_jd(dt)
        assert abs(result_jd - original_jd) < 1e-6

    def test_datetime_roundtrip(self):
        """datetime -> JD -> datetime should return original value."""
        original_dt = datetime.datetime(2024, 6, 15, 14, 30, 45)
        jd = datetime_to_jd(original_dt)
        result_dt = jd_to_datetime(jd)
        # Allow microsecond-level precision loss
        assert abs((result_dt - original_dt).total_seconds()) < 0.001

    def test_roundtrip_various_dates(self):
        """Test round-trip for various dates."""
        test_dates = [
            datetime.datetime(1990, 1, 1, 0, 0, 0),
            datetime.datetime(2000, 12, 31, 23, 59, 59),
            datetime.datetime(2024, 2, 29, 12, 0, 0),  # Leap year
            datetime.datetime(2100, 1, 1, 0, 0, 0),
        ]
        for dt in test_dates:
            jd = datetime_to_jd(dt)
            result = jd_to_datetime(jd)
            assert abs((result - dt).total_seconds()) < 0.001


class TestErrorHandling:
    """Test error handling for invalid inputs."""

    def test_jd_invalid_type_string(self):
        """Test TypeError for string input to jd_to_datetime."""
        with pytest.raises(TypeError):
            jd_to_datetime("not a number")

    def test_jd_invalid_type_none(self):
        """Test TypeError for None input to jd_to_datetime."""
        with pytest.raises(TypeError):
            jd_to_datetime(None)

    def test_datetime_invalid_type(self):
        """Test TypeError for non-datetime input to datetime_to_jd."""
        with pytest.raises(TypeError):
            datetime_to_jd("2000-01-01")

    def test_datetime_invalid_type_none(self):
        """Test TypeError for None input to datetime_to_jd."""
        with pytest.raises(TypeError):
            datetime_to_jd(None)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_large_jd(self):
        """Test large Julian day number (far future)."""
        # Year 3000
        dt = jd_to_datetime(2816787.5)
        assert dt.year == 3000
        assert dt.month == 1
        assert dt.day == 1

    def test_year_boundary(self):
        """Test year boundaries."""
        # New Year's Day
        dt = jd_to_datetime(2451544.5)  # 2000-01-01 00:00:00
        assert dt == datetime.datetime(2000, 1, 1, 0, 0, 0)

    def test_leap_year(self):
        """Test leap year date."""
        dt = datetime.datetime(2000, 2, 29, 12, 0, 0)
        jd = datetime_to_jd(dt)
        result = jd_to_datetime(jd)
        assert result.year == 2000
        assert result.month == 2
        assert result.day == 29

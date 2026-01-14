# tests/test_core.py
# test_kelvin_stardate.py (v1.5-)

from datetime import date
import pytest

from kelvin_stardate.core import (
    earth_to_stardate,
    stardate_to_earth,
    earth_to_stardate_astronomical,
    stardate_to_earth_astronomical,
    KelvinStardate,
    is_leap_year,
)


def test_is_leap_year_basic():
    assert is_leap_year(2020)
    assert not is_leap_year(2019)
    assert is_leap_year(2000)
    assert not is_leap_year(2100)


# Canon examples from Wikipedia / Orci explanations

def test_2258_42_feb_11_no_leap():
    dt = date(2258, 2, 11)
    sd = earth_to_stardate(dt, leap_mode="no_leap")
    assert str(sd) == "2258.42"

    back = stardate_to_earth("2258.42", leap_mode="no_leap")
    assert back == dt


def test_2259_55_feb_24_no_leap():
    dt = date(2259, 2, 24)
    sd = earth_to_stardate(dt, leap_mode="no_leap")
    assert str(sd) == "2259.55"

    back = stardate_to_earth("2259.55", leap_mode="no_leap")
    assert back == dt


def test_2263_02_jan_2_no_leap():
    dt = date(2263, 1, 2)
    sd = earth_to_stardate(dt, leap_mode="no_leap")
    assert str(sd) == "2263.02"

    back = stardate_to_earth("2263.02", leap_mode="no_leap")
    assert back == dt


def test_2233_04_jan_4_no_leap():
    dt = date(2233, 1, 4)
    sd = earth_to_stardate(dt, leap_mode="no_leap")
    assert str(sd) == "2233.04"

    back = stardate_to_earth("2233.04", leap_mode="no_leap")
    assert back == dt


def test_2230_06_jan_6_no_leap():
    dt = date(2230, 1, 6)
    sd = earth_to_stardate(dt, leap_mode="no_leap")
    assert str(sd) == "2230.06"

    back = stardate_to_earth("2230.06", leap_mode="no_leap")
    assert back == dt


# Leap year behavior around 2260 (divisible by 4, not a century year → leap)

def test_leap_year_mode_difference():
    # 2260 is a leap year
    assert is_leap_year(2260)

    dt = date(2260, 3, 1)

    # Gregorian mode: true ordinal
    sd_g = earth_to_stardate(dt, leap_mode="gregorian")
    # Jan (31) + Feb (29) + Mar1(1) = 61 → '2260.61'
    assert str(sd_g) == "2260.61"
    back_g = stardate_to_earth(str(sd_g), leap_mode="gregorian")
    assert back_g == dt

    # No-leap mode: compressed to 365 days
    sd_nl = earth_to_stardate(dt, leap_mode="no_leap")
    # expect 61 - 1 = 60 → '2260.60'
    assert str(sd_nl) == "2260.60"
    back_nl = stardate_to_earth(str(sd_nl), leap_mode="no_leap")
    assert back_nl == dt


def test_parse_and_format_padding():
    # Accepts short decimal, normalizes padding on __str__
    sd = KelvinStardate.parse("2258.4")
    assert sd.year == 2258
    assert sd.ordinal_day == 4
    assert str(sd) == "2258.04"


# --- Astronomical Mode tests ---

def test_astronomical_forward_backward_basic():
    dt = date(2258, 2, 11)  # day 42
    sd = earth_to_stardate_astronomical(dt)
    back = stardate_to_earth_astronomical(sd)
    assert back == dt


def test_astronomical_known_value():
    dt = date(2258, 2, 11)
    sd = earth_to_stardate_astronomical(dt)
    # Expected approximately:
    # 2258 + (42 / 365.2425) = 2258.11499
    assert abs(sd - 2258.11499) < 0.0002


def test_astronomical_leap_year_has_no_offset():
    dt1 = date(2260, 2, 28)
    dt2 = date(2260, 3, 1)
    sd1 = earth_to_stardate_astronomical(dt1)
    sd2 = earth_to_stardate_astronomical(dt2)

    # Leap year: Feb 28 = doy 59, Mar 1 = doy 61 → delta = 2 days
    expected_delta = 2 / 365.2425
    assert abs((sd2 - sd1) - expected_delta) < 1e-5


def test_astronomical_requires_float_stardate_input():
    # Ensure ordinal stardates are rejected in astronomical mode
    with pytest.raises(Exception):
        stardate_to_earth("2258.42", leap_mode="astronomical")

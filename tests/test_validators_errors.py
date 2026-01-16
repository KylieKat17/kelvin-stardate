import pytest

from kelvin_stardate.errors import StardateCLIError
from kelvin_stardate.validators import (
    parse_year_yyyy,
    parse_earth_date,
    validate_stardate_string,
    validate_kelvin_stardate_string,
    parse_month,
    parse_day,
)


def assert_cli_error(excinfo, code: str, contains: str | None = None):
    err = excinfo.value
    assert isinstance(err, StardateCLIError)
    assert err.code == code
    if contains is not None:
        assert contains in err.msg


# ----------------------------
# E001 — Empty input
# ----------------------------

def test_validate_stardate_empty_raises_E001():
    with pytest.raises(StardateCLIError) as excinfo:
        validate_stardate_string("   ")
    assert_cli_error(excinfo, "E001")


# ----------------------------
# E007 — Year formatting
# ----------------------------

def test_parse_year_yyyy_non_numeric_raises_E007():
    with pytest.raises(StardateCLIError) as excinfo:
        parse_year_yyyy("22A8")
    assert_cli_error(excinfo, "E007", "numeric")


def test_parse_year_yyyy_wrong_length_raises_E007():
    with pytest.raises(StardateCLIError) as excinfo:
        parse_year_yyyy("225")
    assert_cli_error(excinfo, "E007", "4 digits")


# ----------------------------
# E012 — Bad Earth date string format
# ----------------------------

def test_parse_earth_date_bad_format_raises_E012():
    with pytest.raises(StardateCLIError) as excinfo:
        parse_earth_date("2258/02/11")  # wrong delimiter
    assert_cli_error(excinfo, "E012", "Expected YYYY-MM-DD")


# ----------------------------
# E003 — Leap-day misuse via injected leap rule
# ----------------------------

def test_parse_earth_date_nonleap_feb29_raises_E003():
    def fake_is_leap_year(y: int) -> bool:
        return False

    with pytest.raises(StardateCLIError) as excinfo:
        parse_earth_date("2260-02-29", is_leap_year_fn=fake_is_leap_year)
    assert_cli_error(excinfo, "E003", "not a leap year")


# ----------------------------
# E011 — Stardate looks like Earth date / malformed
# ----------------------------

def test_validate_stardate_hyphen_raises_E011():
    with pytest.raises(StardateCLIError) as excinfo:
        validate_stardate_string("2258-02-11")
    assert_cli_error(excinfo, "E011", "Earth date detected")


def test_validate_stardate_multiple_decimals_raises_E011():
    with pytest.raises(StardateCLIError) as excinfo:
        validate_stardate_string("2258.04.2")
    assert_cli_error(excinfo, "E011", "exactly one decimal")


def test_validate_kelvin_stardate_wrong_ordinal_digits_raises_E011():
    with pytest.raises(StardateCLIError) as excinfo:
        validate_kelvin_stardate_string("2258.42")  # needs 3-digit ordinal for Kelvin validator
    assert_cli_error(excinfo, "E011", "expected 3-digit ordinal")


def test_validate_kelvin_stardate_ordinal_out_of_range_raises_E011():
    with pytest.raises(StardateCLIError) as excinfo:
        validate_kelvin_stardate_string("2258.999")
    assert_cli_error(excinfo, "E011", "001–366")


# ----------------------------
# E002 — month/day parsing errors (preserving current codes)
# ----------------------------

def test_parse_month_invalid_raises_E002():
    with pytest.raises(StardateCLIError) as excinfo:
        parse_month("monthy")
    assert_cli_error(excinfo, "E002")


def test_parse_day_non_numeric_raises_E002():
    with pytest.raises(StardateCLIError) as excinfo:
        parse_day("two")
    assert_cli_error(excinfo, "E002")

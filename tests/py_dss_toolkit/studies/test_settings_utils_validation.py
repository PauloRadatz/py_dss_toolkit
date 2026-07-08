import re

import pytest

from py_dss_toolkit.studies import settings_utils


class FakeModeDSS:
    def __init__(self, mode: str):
        self.mode = mode
        self.commands = []

    def text(self, command: str):
        self.commands.append(command)
        if command.lower() == "get mode":
            return self.mode
        if command.lower().startswith("set mode="):
            self.mode = command.split("=", 1)[1]
            return ""
        return ""


def test_validate_mode_accepts_mixed_case_and_returns_lowercase():
    actual = settings_utils.validate_mode("DaIlY", settings_utils.VALID_TIMESERIES_MODES)
    assert actual == "daily"


def test_validate_algorithm_accepts_mixed_case_and_returns_lowercase():
    actual = settings_utils.validate_algorithm("NeWtOn")
    assert actual == "newton"


def test_validate_mode_raises_for_invalid_value():
    msg = "Invalid value for mode. Should be one of the following options: ['daily', 'yearly', 'dutycycle']."
    with pytest.raises(ValueError, match=re.escape(msg)):
        settings_utils.validate_mode("snap", settings_utils.VALID_TIMESERIES_MODES)


def test_validate_algorithm_raises_for_invalid_value():
    msg = "Invalid value for algorithm. Should be one of the following options: ['normal', 'newton', 'ncim']."
    with pytest.raises(ValueError, match=re.escape(msg)):
        settings_utils.validate_algorithm("fdlf")


def test_validate_number_accepts_one_as_boundary():
    settings_utils.validate_number(1)


def test_validate_number_raises_for_zero():
    with pytest.raises(ValueError, match="Invalid number value. It should be greater than 0."):
        settings_utils.validate_number(0)


def test_validate_stepsize_accepts_one_as_boundary():
    settings_utils.validate_stepsize(1)


def test_validate_stepsize_raises_for_zero():
    with pytest.raises(ValueError, match="Invalid stepsize value. It should be greater than 0."):
        settings_utils.validate_stepsize(0)


def test_validate_time_accepts_tuple_and_list_with_numeric_values():
    settings_utils.validate_time((1, 0))
    settings_utils.validate_time([1.5, 30])


def test_validate_time_raises_for_invalid_shape_or_type():
    with pytest.raises(ValueError, match="Invalid time format. Expected a tuple or list with two numerical values."):
        settings_utils.validate_time((1, 2, 3))
    with pytest.raises(ValueError, match="Invalid time format. Expected a tuple or list with two numerical values."):
        settings_utils.validate_time(("1", 2))


def test_check_mode_sets_default_when_current_mode_is_invalid():
    dss = FakeModeDSS(mode="invalid")

    mode = settings_utils.check_mode(dss=dss, valid_modes=settings_utils.VALID_TIMESERIES_MODES)

    assert mode == "daily"
    assert "set mode=daily" in dss.commands


def test_set_mode_writes_validated_mode_to_dss():
    dss = FakeModeDSS(mode="daily")

    mode = settings_utils.set_mode(dss=dss, valid_modes=settings_utils.VALID_TIMESERIES_MODES, value="YeArLy")

    assert mode == "yearly"
    assert dss.mode == "yearly"
    assert dss.commands[-1] == "set mode=yearly"

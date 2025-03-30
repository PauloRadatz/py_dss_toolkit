import pytest
import re
import pandas as pd
from untils import expected_outputs

def test_get_mode(timeseries_study_13bus):
    mode = timeseries_study_13bus.settings.mode
    assert mode == "daily"

def test_set_mode_valid_1(timeseries_study_13bus):
    timeseries_study_13bus.settings.mode = "Daily"
    mode = timeseries_study_13bus.settings.mode
    assert mode == "daily"

def test_set_mode_valid_2(timeseries_study_13bus):
    timeseries_study_13bus.settings.mode = "Dutycycle"
    mode = timeseries_study_13bus.settings.mode
    assert mode == "dutycycle"

def test_set_mode_valid_3(timeseries_study_13bus):
    timeseries_study_13bus.settings.mode = "Yearly"
    mode = timeseries_study_13bus.settings.mode
    assert mode == "yearly"

def test_set_mode_dss(timeseries_study_13bus):
    timeseries_study_13bus.dss.text("set mode=Yearly")
    mode = timeseries_study_13bus.settings.mode
    assert mode == "yearly"

def test_set_mode_not_valid(timeseries_study_13bus):
    msg = "Invalid value for mode. Should be one of the following options: ['daily', 'yearly', 'dutycycle']."
    with pytest.raises(ValueError, match=re.escape(msg)):
        timeseries_study_13bus.settings.mode = "snap"

def test_get_number(timeseries_study_13bus):
    number = timeseries_study_13bus.settings.number
    assert number == 24

def test_set_number(timeseries_study_13bus):
    timeseries_study_13bus.settings.number = 2
    number = timeseries_study_13bus.settings.number
    assert number == 2

def test_set_number_dss(timeseries_study_13bus):
    timeseries_study_13bus.dss.text("set number=2")
    number = timeseries_study_13bus.settings.number
    assert number == 2

def test_get_stepsize(timeseries_study_13bus):
    stepsize = timeseries_study_13bus.settings.stepsize
    assert stepsize == 3600

def test_set_stepsize(timeseries_study_13bus):
    timeseries_study_13bus.settings.stepsize = 2
    stepsize = timeseries_study_13bus.settings.stepsize
    assert stepsize == 2

def test_set_stepsize_dss(timeseries_study_13bus):
    timeseries_study_13bus.dss.text("set stepsize=2h")
    stepsize = timeseries_study_13bus.settings.stepsize
    assert stepsize == 3600 * 2

def test_get_time(timeseries_study_13bus):
    time = timeseries_study_13bus.settings.time
    assert time == (0, 0)

def test_set_time(timeseries_study_13bus):
    timeseries_study_13bus.settings.time = (3, 0)
    time = timeseries_study_13bus.settings.time
    assert time == (3, 0)

def test_set_time_dss_1(timeseries_study_13bus):
    timeseries_study_13bus.dss.text("set hour=3")
    time = timeseries_study_13bus.settings.time
    assert time == (3, 0)

def test_set_time_dss_2(timeseries_study_13bus):
    timeseries_study_13bus.dss.text("set time=(3, 0)")
    time = timeseries_study_13bus.settings.time
    assert time == (3, 0)

def test_get_settings(timeseries_study_13bus):
    actual = timeseries_study_13bus.settings.get_settings().loc["mode", "Settings"]
    expected = pd.read_csv(expected_outputs.joinpath("timeseries_settings_13bus.csv"), index_col=0).loc["mode", "Settings"]
    assert actual == expected

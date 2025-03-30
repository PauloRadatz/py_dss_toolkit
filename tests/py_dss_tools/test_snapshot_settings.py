import pytest
import re
import pandas as pd
from untils import expected_outputs

def test_get_mode(snapshot_study_13bus):
    mode = snapshot_study_13bus.settings.mode
    assert mode == "snap"

def test_set_mode_valid(snapshot_study_13bus):
    snapshot_study_13bus.settings.mode = "Snapshot"
    mode = snapshot_study_13bus.settings.mode
    assert mode == "snap"

def test_set_mode_valid_dss(snapshot_study_13bus):
    snapshot_study_13bus.dss.text("set mode=snap")
    mode = snapshot_study_13bus.settings.mode
    assert mode == "snap"

def test_set_mode_not_valid(snapshot_study_13bus):
    msg = "Invalid value for mode. Should be one of the following options: ['snapshot', 'snap']."
    with pytest.raises(ValueError, match=re.escape(msg)):
        snapshot_study_13bus.settings.mode = "daily"


def test_get_settings(snapshot_study_13bus):
    actual = snapshot_study_13bus.settings.get_settings().loc["mode", "Settings"]
    expected = pd.read_csv(expected_outputs.joinpath("snapshot_settings_13bus.csv"), index_col=0).loc["mode", "Settings"]
    assert actual == expected

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from untils import expected_outputs

from py_dss_toolkit import dss_tools


def assert_normal_current_loading_percent_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("results_normal_current_loading_percent_13bus.parquet"))
    assert_frame_equal(df, expected_df)


def assert_emerg_current_loading_percent_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("results_emerg_current_loading_percent_13bus.parquet"))
    assert_frame_equal(df, expected_df)


def test_dss_tools_13bus_current_loading_percent_norm(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dss_tools.results.set_violation_current_limit_type("norm_amps")
    df = dss_tools.results.current_loading_percent
    assert_normal_current_loading_percent_13bus(df)


def test_dss_tools_13bus_current_loading_percent_emerg(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dss_tools.results.set_violation_current_limit_type("emerg_amps")
    df = dss_tools.results.current_loading_percent
    assert_emerg_current_loading_percent_13bus(df)


def test_snapshot_13bus_current_loading_percent_norm(snapshot_study_13bus):
    snapshot_study_13bus.run()
    snapshot_study_13bus.results.set_violation_current_limit_type("norm_amps")
    df = snapshot_study_13bus.results.current_loading_percent
    assert_normal_current_loading_percent_13bus(df)


def test_snapshot_13bus_current_loading_percent_emerg(snapshot_study_13bus):
    snapshot_study_13bus.run()
    snapshot_study_13bus.results.set_violation_current_limit_type("emerg_amps")
    df = snapshot_study_13bus.results.current_loading_percent
    assert_emerg_current_loading_percent_13bus(df)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_loading_current_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_shape = study.results.current_loading_percent.shape
    # Adjust shape as appropriate for your output
    assert df_shape[1] > 0

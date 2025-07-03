import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from py_dss_toolkit import dss_tools
from untils import expected_outputs

def assert_violation_under_voltage_ln_nodes_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("results_violation_under_voltage_ln_nodes_13bus.parquet"))
    assert_frame_equal(df, expected_df)

def test_dss_tools_13bus_violation_under_voltage_ln_nodes(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    df = dss_tools.results.violation_voltage_ln_nodes[0]
    assert_violation_under_voltage_ln_nodes_13bus(df)

def test_snapshot_13bus_violation_under_voltage_ln_nodes(snapshot_study_13bus):
    snapshot_study_13bus.run()
    df = snapshot_study_13bus.results.violation_voltage_ln_nodes[0]
    assert_violation_under_voltage_ln_nodes_13bus(df)

def assert_violation_over_voltage_ln_nodes_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("results_violation_over_voltage_ln_nodes_13bus.parquet"))
    assert_frame_equal(df, expected_df)

def test_dss_tools_13bus_violation_over_voltage_ln_nodes(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    df = dss_tools.results.violation_voltage_ln_nodes[1]
    assert_violation_over_voltage_ln_nodes_13bus(df)

def test_snapshot_13bus_violation_over_voltage_ln_nodes(snapshot_study_13bus):
    snapshot_study_13bus.run()
    df = snapshot_study_13bus.results.violation_voltage_ln_nodes[1]
    assert_violation_over_voltage_ln_nodes_13bus(df)

@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_violation_voltage_ln_nodes_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_shape = study.results.violation_voltage_ln_nodes[0].shape
    # Adjust shape as appropriate for your output
    assert df_shape[1] > 0

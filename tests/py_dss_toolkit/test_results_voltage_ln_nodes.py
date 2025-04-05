import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from py_dss_toolkit import dss_tools
from untils import expected_outputs


def assert_voltage_ln_nodes_13bus(dfs):
    expected_vmag_df = pd.read_parquet(expected_outputs.joinpath("results_vmag_ln_nodes_13bus.parquet"))
    expected_vang_df = pd.read_parquet(expected_outputs.joinpath("results_vang_ln_nodes_13bus.parquet"))
    assert_frame_equal(dfs[0], expected_vmag_df)
    assert_frame_equal(dfs[1], expected_vang_df)


def test_dss_tools_13bus_results_voltage_ln_nodes(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dfs = dss_tools.results.voltage_ln_nodes
    assert_voltage_ln_nodes_13bus(dfs)


def test_snapshot_13bus_results_voltage_ln_nodes(snapshot_study_13bus):
    snapshot_study_13bus.run()
    dfs = snapshot_study_13bus.results.voltage_ln_nodes
    assert_voltage_ln_nodes_13bus(dfs)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_results_voltage_ln_nodes_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_mag_shape = study.results.voltage_ln_nodes[0].shape
    df_ang_shape = study.results.voltage_ln_nodes[1].shape
    assert df_mag_shape == (16, 3)
    assert df_ang_shape == (16, 3)

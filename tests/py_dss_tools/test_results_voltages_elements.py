import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from py_dss_tools import dss_tools
from untils import expected_outputs


def assert_voltages_elements_13bus(dfs):
    expected_mag_df = pd.read_parquet(expected_outputs.joinpath("results_mag_voltages_elements_13bus.parquet"))
    expected_ang_df = pd.read_parquet(expected_outputs.joinpath("results_ang_voltages_elements_13bus.parquet"))
    assert_frame_equal(dfs[0], expected_mag_df)
    assert_frame_equal(dfs[1], expected_ang_df)


def test_dss_tools_13bus_results_voltages_elements(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dfs = dss_tools.results.voltages_elements
    assert_voltages_elements_13bus(dfs)


def test_snapshot_13bus_results_voltages_elements(snapshot_study_13bus):
    snapshot_study_13bus.run()
    dfs = snapshot_study_13bus.results.voltages_elements
    assert_voltages_elements_13bus(dfs)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_results_voltages_elements_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_p_shape = study.results.voltages_elements[0].shape
    df_q_shape = study.results.voltages_elements[1].shape
    assert df_p_shape == (34, 8)
    assert df_q_shape == (34, 8)

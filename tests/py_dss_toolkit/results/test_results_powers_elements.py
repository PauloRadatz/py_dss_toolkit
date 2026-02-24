import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from py_dss_toolkit import dss_tools
from untils import expected_outputs


def assert_powers_elements_13bus(dfs):
    expected_p_df = pd.read_parquet(expected_outputs.joinpath("results_p_power_elements_13bus.parquet"))
    expected_q_df = pd.read_parquet(expected_outputs.joinpath("results_q_power_elements_13bus.parquet"))
    assert_frame_equal(dfs[0], expected_p_df)
    assert_frame_equal(dfs[1], expected_q_df)


def test_dss_tools_13bus_results_powers_elements(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dfs = dss_tools.results.powers_elements
    assert_powers_elements_13bus(dfs)


def test_snapshot_13bus_results_powers_elements(snapshot_study_13bus):
    snapshot_study_13bus.run()
    dfs = snapshot_study_13bus.results.powers_elements
    assert_powers_elements_13bus(dfs)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_results_powers_elements_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_p_shape = study.results.powers_elements[0].shape
    df_q_shape = study.results.powers_elements[1].shape
    assert df_p_shape == (34, 8)
    assert df_q_shape == (34, 8)

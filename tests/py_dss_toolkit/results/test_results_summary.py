import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from untils import expected_outputs

from py_dss_toolkit import dss_tools


def assert_summary_df_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("results_summary_df_13bus.parquet"))
    assert_frame_equal(df, expected_df)


def test_dss_tools_13bus_results_summary_df(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    df = dss_tools.results.summary_df
    assert_summary_df_13bus(df)


def test_snapshot_13bus_results_summary_df(snapshot_study_13bus):
    snapshot_study_13bus.run()
    df = snapshot_study_13bus.results.summary_df
    assert_summary_df_13bus(df)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_results_summary_df_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_shape = study.results.summary_df.shape
    assert df_shape == (6, 1)

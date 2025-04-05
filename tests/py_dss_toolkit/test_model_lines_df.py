import pytest
from py_dss_toolkit import dss_tools
import pandas as pd
from untils import expected_outputs
from pandas.testing import assert_frame_equal

def assert_lines_df_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("lines_df_13bus.parquet"))
    assert_frame_equal(df, expected_df)

@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_model_lines_df_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    df = study.model.lines_df
    assert_lines_df_13bus(df)

def test_dss_tools_13bus_model_lines_df(dss_tools_13bus):
    df = dss_tools.model.lines_df
    assert_lines_df_13bus(df)

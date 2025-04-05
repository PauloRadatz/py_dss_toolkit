import pytest
from py_dss_toolkit import dss_tools
import pandas as pd
from untils import expected_outputs
from pandas.testing import assert_frame_equal

def assert_element_data_df_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("element_data_df_13bus.parquet"))
    assert_frame_equal(df, expected_df)

@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_model_element_data_df_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    df = study.model.element_data("line", "632633")
    assert_element_data_df_13bus(df)

def test_dss_tools_13bus_model_element_data_df(dss_tools_13bus):
    df = dss_tools.model.element_data("line", "632633")
    assert_element_data_df_13bus(df)

def test_dss_tools_13bus_model_edit_element_data_df(dss_tools_13bus):
    dss_tools.model.edit_element("line", "632633", dict(normamps=800, emergamps=1000))
    df = dss_tools.model.element_data("line", "632633")

    assert df.loc["normamps", "632633"] == '800'
    assert df.loc["emergamps", "632633"] == '1000'

def test_dss_tools_13bus_model_element_element_not_found(dss_tools_13bus):
    with pytest.raises(ValueError, match=r"line.TEST does not have exist in the model"):
        dss_tools.model.element_data("line", "TEST")

def test_dss_tools_13bus_model_edit_element_element_not_found(dss_tools_13bus):
    with pytest.raises(ValueError, match=r"line.TEST does not have exist in the model"):
        dss_tools.model.edit_element("line", "TEST", dict(normamps=800, emergamps=1000))

def test_dss_tools_13bus_model_edit_element_property_not_found(dss_tools_13bus):
    with pytest.raises(ValueError, match=r"line.632633 does not have property test_property"):
        dss_tools.model.edit_element("line", "632633", dict(test_property=800, emergamps=1000))

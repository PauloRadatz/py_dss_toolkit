import pytest
from py_dss_tools import dss_tools
import pandas as pd
from untils import expected_outputs
from pandas.testing import assert_frame_equal

def assert_energymeters_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("results_energymeters_13bus.parquet"))
    assert_frame_equal(df, expected_df)


def test_dss_tools_13bus_results_energymeters(dss_tools_13bus):
    dss_tools.model.add_line_in_vsource(add_meter=True)
    dss_tools.simulation.solve_daily()
    df = dss_tools.results.energymeters
    assert_energymeters_13bus(df)

def test_snapshot_13bus_results_energymeters(timeseries_study_13bus):
    timeseries_study_13bus.model.add_line_in_vsource(add_meter=True)
    timeseries_study_13bus.run()
    df = timeseries_study_13bus.results.energymeters
    assert_energymeters_13bus(df)

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from py_dss_tools import dss_tools
from untils import expected_outputs


def assert_monitor_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("results_monitor_1_13bus.parquet"))
    assert_frame_equal(df, expected_df)


def test_dss_tools_13bus_results_monitor(dss_tools_13bus):
    dss_tools.model.add_line_in_vsource(add_monitors=True)
    dss_tools.simulation.solve_daily()
    df = dss_tools.results.monitor("monitor_feeder_head_pq")
    assert_monitor_13bus(df)


def test_snapshot_13bus_results_monitor(timeseries_study_13bus):
    timeseries_study_13bus.model.add_line_in_vsource(add_monitors=True)
    timeseries_study_13bus.run()
    df = timeseries_study_13bus.results.monitor("monitor_feeder_head_pq")
    assert_monitor_13bus(df)


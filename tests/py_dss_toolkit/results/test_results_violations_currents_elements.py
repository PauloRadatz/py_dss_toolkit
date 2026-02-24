import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from py_dss_toolkit import dss_tools
from untils import expected_outputs

def assert_violations_currents_elements_13bus(df, expected_file):
    expected_df = pd.read_parquet(expected_outputs.joinpath(expected_file))
    assert_frame_equal(df, expected_df)

def test_dss_tools_13bus_violations_currents_elements_norm(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dss_tools.results.set_violation_current_limit_type("norm_amps")
    df = dss_tools.results.violation_currents_elements
    assert_violations_currents_elements_13bus(df, "results_violations_currents_elements_norm_13bus.parquet")

def test_dss_tools_13bus_violations_currents_elements_emerg(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dss_tools.results.set_violation_current_limit_type("emerg_amps")
    df = dss_tools.results.violation_currents_elements
    assert_violations_currents_elements_13bus(df, "results_violations_currents_elements_emerg_13bus.parquet")

def test_snapshot_13bus_violations_currents_elements_norm(snapshot_study_13bus):
    snapshot_study_13bus.run()
    snapshot_study_13bus.results.set_violation_current_limit_type("norm_amps")
    df = snapshot_study_13bus.results.violation_currents_elements
    assert_violations_currents_elements_13bus(df, "results_violations_currents_elements_norm_13bus.parquet")

def test_snapshot_13bus_violations_currents_elements_emerg(snapshot_study_13bus):
    snapshot_study_13bus.run()
    snapshot_study_13bus.results.set_violation_current_limit_type("emerg_amps")
    df = snapshot_study_13bus.results.violation_currents_elements
    assert_violations_currents_elements_13bus(df, "results_violations_currents_elements_emerg_13bus.parquet")

@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_violation_loading_current_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_shape = study.results.current_loading_percent.shape
    # Adjust shape as appropriate for your output
    assert df_shape[1] > 0

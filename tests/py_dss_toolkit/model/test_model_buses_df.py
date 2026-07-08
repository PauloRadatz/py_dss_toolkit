import pandas as pd
import py_dss_interface
import pytest
from pandas.testing import assert_frame_equal
from untils import expected_outputs

from py_dss_toolkit import dss_tools


def _run_dss_script(script: str):
    """Run DSS script string via dss.text() and return DSS instance."""
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())
    return dss


# Simple circuit: A -> B -> C, all elements enabled
SCRIPT_SIMPLE_ALL_ENABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3
New Line.Second bus1=B bus2=C phases=3
New load.l bus1=C kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# Same circuit but Line.Second disabled: A -> B, C is at far end of disabled line
SCRIPT_SIMPLE_LINE_DISABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3
New Line.Second bus1=B bus2=C phases=3 enabled=no
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def assert_buses_df_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("buses_df_13bus.parquet"))
    assert_frame_equal(df, expected_df)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_model_buses_df_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    df = study.model.buses_df
    assert_buses_df_13bus(df)


def test_dss_tools_13bus_model_buses_df(dss_tools_13bus):
    df = dss_tools.model.buses_df
    assert_buses_df_13bus(df)


def test_buses_df_simple_circuit_all_enabled():
    _run_dss_script(SCRIPT_SIMPLE_ALL_ENABLED)
    df = dss_tools.model.buses_df
    bus_names = set(df["name"].str.lower())
    assert "a" in bus_names
    assert "b" in bus_names
    assert "c" in bus_names


def test_buses_df_simple_circuit_line_disabled():
    _run_dss_script(SCRIPT_SIMPLE_LINE_DISABLED)
    df = dss_tools.model.buses_df
    bus_names = set(df["name"].str.lower())
    assert "a" in bus_names
    assert "b" in bus_names
    assert "c" not in bus_names, "Bus C (far end of disabled line) should not appear in buses_df"

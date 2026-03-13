import pytest
import py_dss_interface
from py_dss_toolkit import dss_tools
import pandas as pd
from untils import expected_outputs
from pandas.testing import assert_frame_equal


def _run_dss_script(script: str):
    """Run DSS script string via dss.text() and return DSS instance."""
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())
    return dss


# Simple circuit: A -> B -> C, both lines enabled
SCRIPT_LINES_ENABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3
New Line.Second bus1=B bus2=C phases=3
New load.l bus1=C kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# Same circuit but Line.Second disabled
SCRIPT_LINE_DISABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 length=1
New Line.Second bus1=B bus2=C phases=3 enabled=no
New load.l bus1=C kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# Circuit with no lines (transformer only)
SCRIPT_NO_LINES = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kV=13.8 kva=300 conn=delta
~ wdg=2 bus=B kV=0.22 kva=300 conn=wye
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""


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


def test_lines_df_simple_circuit_all_lines_enabled():
    """lines_df includes all lines when all are enabled."""
    _run_dss_script(SCRIPT_LINES_ENABLED)
    df = dss_tools.model.lines_df
    assert df is not None
    line_names = set(df["name"].str.lower())
    assert "main" in line_names
    assert "second" in line_names
    assert len(df) == 2


def test_lines_df_simple_circuit_disabled_line_excluded():
    """lines_df excludes disabled lines; only enabled lines appear."""
    _run_dss_script(SCRIPT_LINE_DISABLED)
    df = dss_tools.model.lines_df
    assert df is not None
    line_names = set(df["name"].str.lower())
    assert "main" in line_names
    assert "second" not in line_names, "Disabled Line.Second should not appear in lines_df"
    assert len(df) == 1


def test_lines_df_empty_when_no_lines_in_model():
    """lines_df is None when there are no lines in the circuit."""
    _run_dss_script(SCRIPT_NO_LINES)
    df = dss_tools.model.lines_df
    assert df is None

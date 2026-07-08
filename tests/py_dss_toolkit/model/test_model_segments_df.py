import pandas as pd
import pytest
from _dss_script_runner import run_dss_script
from pandas.testing import assert_frame_equal
from untils import expected_outputs

from py_dss_toolkit import dss_tools

SCRIPT_SEGMENTS_ENABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 length=1
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=B kV=13.8 kva=300 conn=delta
~ wdg=2 bus=C kV=0.22 kva=300 conn=wye
New load.l bus1=C kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_SEGMENT_DISABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 length=1
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2 enabled=no
~ wdg=1 bus=B kV=13.8 kva=300 conn=delta
~ wdg=2 bus=C kV=0.22 kva=300 conn=wye
New load.l bus1=C kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_NO_SEGMENTS = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New load.l bus1=A kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def assert_segments_df_13bus(df):
    expected_df = pd.read_parquet(expected_outputs.joinpath("segments_df_13bus.parquet"))
    assert_frame_equal(df, expected_df)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_model_segments_df_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    df = study.model.segments_df
    assert_segments_df_13bus(df)


def test_dss_tools_13bus_model_segments_df(dss_tools_13bus):
    df = dss_tools.model.segments_df
    assert_segments_df_13bus(df)


def test_segments_df_simple_circuit_all_segments_enabled():
    """segments_df includes enabled line and transformer segments only."""
    run_dss_script(SCRIPT_SEGMENTS_ENABLED)
    df = dss_tools.model.segments_df

    assert df is not None
    segment_names = set(df["name"].str.lower())

    assert "line.main" in segment_names
    assert "transformer.t1" in segment_names
    assert "enabled" in df.columns
    assert len(df) == 2


def test_segments_df_simple_circuit_disabled():
    """segments_df excludes disabled segments entirely."""
    run_dss_script(SCRIPT_SEGMENT_DISABLED)
    df = dss_tools.model.segments_df

    assert df is not None
    segment_names = set(df["name"].str.lower())

    assert "line.main" in segment_names
    assert "transformer.t1" in segment_names
    assert "enabled" in df.columns
    assert len(df) == 2


def test_disabled_segments_df_simple_circuit_exposes_disabled_only():
    """disabled_segments_df includes only disabled segments."""
    run_dss_script(SCRIPT_SEGMENT_DISABLED)
    df = dss_tools.model.disabled_segments_df

    assert df is not None
    segment_names = set(df["name"].str.lower())

    assert "transformer.t1" in segment_names
    assert "line.main" not in segment_names
    assert "enabled" not in df.columns
    assert len(df) == 1


def test_segments_df_empty_when_no_segments_in_model():
    """segments_df is None when the circuit has no segments."""
    run_dss_script(SCRIPT_NO_SEGMENTS)
    df = dss_tools.model.segments_df

    assert df is None


def test_disabled_segments_df_empty_when_all_segments_enabled():
    """disabled_segments_df is None when all segments are enabled."""
    run_dss_script(SCRIPT_SEGMENTS_ENABLED)
    df = dss_tools.model.disabled_segments_df

    assert df is None

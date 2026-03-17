# -*- coding: utf-8 -*-
"""Tests for reversed_segments_df."""

from py_dss_toolkit import dss_tools

from .helpers import run_dss_script

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_REVERSED_LINE = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=B bus2=A phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_NO_REVERSED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_reversed_segments_df_filters_graph_df():
    """reversed_segments_df filters graph_df for reversed edges."""
    run_dss_script(SCRIPT_REVERSED_LINE)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    model = dss_tools.model
    mv_df = mv.reversed_segments_df
    expected = model.graph_df[model.graph_df["reversed"]].reset_index(drop=True)
    assert mv_df.equals(expected)


def test_reversed_segments_df_has_reversed_true():
    """Reversed line should show up with reversed=True."""
    run_dss_script(SCRIPT_REVERSED_LINE)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = mv.reversed_segments_df
    assert len(df) >= 1
    assert (df["reversed"]).all()


def test_reversed_segments_df_bus1_dss_bus2_dss_reflect_model():
    """bus1_dss and bus2_dss reflect DSS/model segment order, not graph direction."""
    run_dss_script(SCRIPT_REVERSED_LINE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.reversed_segments_df
    assert len(df) >= 1
    row = df.iloc[0]
    assert row["bus1"] == "a" and row["bus2"] == "b"
    assert row["bus1_dss"] == "b" and row["bus2_dss"] == "a"


def test_reversed_segments_df_13bus(dss_tools_13bus):
    """reversed_segments_df filters graph_df on the 13-bus feeder."""
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    model = dss_tools.model
    expected = model.graph_df[model.graph_df["reversed"]].reset_index(drop=True)
    assert mv.reversed_segments_df.equals(expected)


def test_reversed_segments_df_no_reversed_returns_empty():
    """When DSS order matches BFS order, reversed_segments_df is empty."""
    run_dss_script(SCRIPT_NO_REVERSED)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = mv.reversed_segments_df
    assert len(df) == 0

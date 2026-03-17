# -*- coding: utf-8 -*-
"""Tests for loop_edges_df and is_radial."""

from py_dss_toolkit import dss_tools

from .helpers import run_dss_script

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_RADIAL = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_MESHED_LOOP = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.L3 bus1=C bus2=A phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_loop_edges_df_radial_empty():
    """Radial circuit has empty loop_edges_df and is_radial=True."""
    run_dss_script(SCRIPT_RADIAL)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    assert mv.is_radial is True
    assert len(mv.loop_edges_df) == 0


def test_loop_edges_df_meshed_has_edges():
    """Meshed circuit (A-B-C-A loop) has loop-closing segments."""
    run_dss_script(SCRIPT_MESHED_LOOP)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    assert mv.is_radial is False
    df = mv.loop_edges_df
    assert len(df) >= 1
    assert list(df.columns) == ["bus1", "bus2", "name", "type", "cycle_id", "level"]
    assert set(df["name"]) >= {"line.l1", "line.l2", "line.l3"}
    assert set(df["cycle_id"]) == {1}
    assert set(df["level"]) == {1, 2, 3}


def test_is_radial_property():
    """is_radial is True for radial, False for meshed."""
    run_dss_script(SCRIPT_RADIAL)
    dss_tools.model.refresh_graph()
    assert dss_tools.model_verification.is_radial is True
    run_dss_script(SCRIPT_MESHED_LOOP)
    dss_tools.model.refresh_graph()
    assert dss_tools.model_verification.is_radial is False

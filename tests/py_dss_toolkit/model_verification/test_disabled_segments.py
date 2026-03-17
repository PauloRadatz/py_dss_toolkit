# -*- coding: utf-8 -*-
"""Tests for disabled_segments_df (model segment filtering)."""

from py_dss_toolkit import dss_tools

from .helpers import run_dss_script

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_PHASES_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_DISABLED_NOT_ISOLATED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.Off bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1 enabled=no
New load.l1 bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_disabled_segments_df_returns_disabled_only():
    """disabled_segments_df returns only segments with enabled=False."""
    run_dss_script(SCRIPT_DISABLED_NOT_ISOLATED)
    df = dss_tools.model.disabled_segments_df
    assert len(df) >= 1
    assert "line.off" in df["name"].str.lower().values


def test_disabled_segments_df_empty_when_all_enabled():
    """disabled_segments_df is None or empty when all segments are enabled."""
    run_dss_script(SCRIPT_PHASES_OK)
    df = dss_tools.model.disabled_segments_df
    assert df is None or df.empty

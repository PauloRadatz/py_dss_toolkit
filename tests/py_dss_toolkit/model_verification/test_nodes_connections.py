# -*- coding: utf-8 -*-
"""
Unit tests for NodesConnections using OpenDSS circuits.
Each test uses a minimal DSS script to exercise node/phase connection logic.
"""

import py_dss_interface

from py_dss_toolkit import dss_tools


def run_dss_script(script: str):
    """Run DSS script string via dss.text() and return DSS instance."""
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())
    return dss


# ---------------------------------------------------------------------------
# DSS Scripts: subset OK (child phases within parent)
# ---------------------------------------------------------------------------

# 3-phase line and 3-phase load — all match
SCRIPT_3PH_3PH_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# 3-phase line, 2-phase load at B — subset OK
SCRIPT_3PH_2PH_LOAD_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A.1.2.3 bus2=B.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2 phases=2 kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# 3-phase line, 1-phase load at B — subset OK
SCRIPT_3PH_1PH_LOAD_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A.1.2.3 bus2=B.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1 phases=1 kw=30 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# 2-phase line, 1-phase load — subset OK
SCRIPT_2PH_1PH_LOAD_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1 phases=1 kw=30 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# DSS Scripts: child has extra phase (mismatch)
# ---------------------------------------------------------------------------

# 2-phase line, 3-phase load — load has phase 3 that line lacks
SCRIPT_2PH_3PH_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2.3 phases=3 kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# 1-phase line, 2-phase load — load has phase 2 that line lacks
SCRIPT_1PH_2PH_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=1 bus1=A.1 bus2=B.1 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2 phases=2 kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# 2-phase line, 3-phase line downstream — PD mismatch
SCRIPT_2PH_3PH_LINE_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 phases=3 bus1=B.1.2.3 bus2=C.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=C kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# DSS Scripts: default nodes (bus without explicit nodes → 1.2.3)
# ---------------------------------------------------------------------------

# Load at B with bus1=B (no nodes) defaults to 3-phase; 3-phase line — OK
SCRIPT_DEFAULT_NODES_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# Tests: subset OK
# ---------------------------------------------------------------------------


def test_circuit_3ph_3ph_no_issues():
    """3-phase line and 3-phase load — no phase connection issues."""
    run_dss_script(SCRIPT_3PH_3PH_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_circuit_3ph_2ph_load_no_issues():
    """3-phase line, 2-phase load — subset OK, no issues."""
    run_dss_script(SCRIPT_3PH_2PH_LOAD_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_circuit_3ph_1ph_load_no_issues():
    """3-phase line, 1-phase load — subset OK, no issues."""
    run_dss_script(SCRIPT_3PH_1PH_LOAD_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_circuit_2ph_1ph_load_no_issues():
    """2-phase line, 1-phase load — subset OK, no issues."""
    run_dss_script(SCRIPT_2PH_1PH_LOAD_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


# ---------------------------------------------------------------------------
# Tests: child has extra phase (mismatch)
# ---------------------------------------------------------------------------


def test_circuit_2ph_3ph_load_flagged():
    """2-phase line, 3-phase load — load flagged."""
    run_dss_script(SCRIPT_2PH_3PH_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1
    assert load_issues.iloc[0]["element_name"] == "load.l"


def test_circuit_1ph_2ph_load_flagged():
    """1-phase line, 2-phase load — load flagged."""
    run_dss_script(SCRIPT_1PH_2PH_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1


def test_circuit_2ph_3ph_line_flagged():
    """2-phase line feeding 3-phase line — downstream line flagged."""
    run_dss_script(SCRIPT_2PH_3PH_LINE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    pd_issues = df[df["element_name"].str.startswith("line.")]
    assert len(pd_issues) >= 1
    assert "line.l2" in pd_issues["element_name"].values


# ---------------------------------------------------------------------------
# Tests: default nodes
# ---------------------------------------------------------------------------


def test_circuit_default_nodes_no_issues():
    """Load with bus1=B (default nodes) and 3-phase line — no issues."""
    run_dss_script(SCRIPT_DEFAULT_NODES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


# ---------------------------------------------------------------------------
# Tests: propagated check with circuits
# ---------------------------------------------------------------------------

# L1: 2ph A->B, L2: 3ph B->C (flagged), L3: 2ph C->D, load at D.1.2 (2ph)
# Only L2 flagged; L3 and load match validated phases at C/D
SCRIPT_PROPAGATED_NO_CASCADE = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 phases=3 bus1=B.1.2.3 bus2=C.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New Line.L3 phases=2 bus1=C.1.2 bus2=D.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=D.1.2 phases=2 kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_circuit_propagated_no_cascade():
    """Propagated check: L2 flagged; downstream L3 and load not cascaded."""
    run_dss_script(SCRIPT_PROPAGATED_NO_CASCADE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    flagged = set(df["element_name"])
    assert "line.l2" in flagged
    assert "line.l3" not in flagged
    assert "load.l" not in flagged

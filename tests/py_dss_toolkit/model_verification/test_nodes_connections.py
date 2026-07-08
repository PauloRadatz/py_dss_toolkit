# -*- coding: utf-8 -*-
"""Tests for nodes_connections_parent_child_df and nodes_connections_propagated_df."""

from py_dss_toolkit import dss_tools

from .helpers import run_dss_script

# ---------------------------------------------------------------------------
# DSS Scripts: phases OK (child phases within parent)
# ---------------------------------------------------------------------------

SCRIPT_3PH_3PH_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_3PH_2PH_LOAD_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A.1.2.3 bus2=B.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2 phases=1 kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_3PH_1PH_LOAD_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A.1.2.3 bus2=B.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1 phases=1 kw=30 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

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
# DSS Scripts: phase mismatch
# ---------------------------------------------------------------------------

SCRIPT_2PH_3PH_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2.3 phases=3 kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_1PH_2PH_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=1 bus1=A.1 bus2=B.1 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2 phases=2 kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

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

SCRIPT_DEFAULT_NODES_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_PHASES_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_PHASES_PD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 phases=3 bus1=B.1.2.3 bus2=C.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=C kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_PHASES_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2.3 phases=3 kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_PROPAGATED_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2.3 phases=3 kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

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

SCRIPT_PROPAGATED_MULTI_BRANCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.AB phases=3 bus1=A.1.2.3 bus2=B.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New Line.BC phases=2 bus1=B.1.2   bus2=C.1.2   r1=0.1 x1=0.1 c1=0 length=1
New Line.BD phases=1 bus1=B.1     bus2=D.1     r1=0.1 x1=0.1 c1=0 length=1
New Line.CE phases=3 bus1=C.1.2.3 bus2=E.1.2.3 r1=0.1 x1=0.1 c1=0 length=1
New Line.EH phases=1 bus1=E.1     bus2=H.1     r1=0.1 x1=0.1 c1=0 length=1
New Line.DF phases=1 bus1=D.2     bus2=F.2     r1=0.1 x1=0.1 c1=0 length=1
New Line.FG phases=1 bus1=F.1     bus2=G.1     r1=0.1 x1=0.1 c1=0 length=1
New load.lh bus1=H.1 phases=1 kw=10 pf=1
New load.lg bus1=G.1 phases=1 kw=10 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_1PH_SOURCE_OK = """
ClearAll
New Circuit.Thevenin bus1=A.1 pu=1.0 basekv=0.127 phases=1 model=ideal
New Line.Main phases=1 bus1=A.1 bus2=B.1 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1 phases=1 kw=10 pf=1
Set voltagebases=[0.127]
Calcvoltagebases
Solve
"""

SCRIPT_PARALLEL_1PH_XFMR_3PH_LINE = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoA phases=1 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800
~ wdg=1 bus=A.1.2 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.1 kv=0.127 kva=37.5 conn=wye
New Transformer.TrafoB phases=1 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800
~ wdg=1 bus=A.2.3 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.2 kv=0.127 kva=37.5 conn=wye
New Transformer.TrafoC phases=1 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800
~ wdg=1 bus=A.3.1 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.3 kv=0.127 kva=37.5 conn=wye
New Line.L1 bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=C kw=50 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_GENERATOR_PHASE_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New Generator.G1 bus1=B.1.2.3 phases=3 kw=50 pf=1 model=3
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_CAPACITOR_PHASE_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New Capacitor.C1 bus1=B.1.2.3 phases=3 kvar=50
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_DELTA_CAPACITOR_PHASE_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New Capacitor.Cdelta bus1=B phases=3 kvar=50 conn=delta
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# parent_child: OK cases
# ---------------------------------------------------------------------------


def test_parent_child_3ph_3ph_no_issues():
    """3-phase line and 3-phase load — no phase connection issues."""
    run_dss_script(SCRIPT_3PH_3PH_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_parent_child_3ph_2ph_load_no_issues():
    """3-phase line, 2-phase load — subset OK, no issues."""
    run_dss_script(SCRIPT_3PH_2PH_LOAD_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_parent_child_3ph_1ph_load_no_issues():
    """3-phase line, 1-phase load — subset OK, no issues."""
    run_dss_script(SCRIPT_3PH_1PH_LOAD_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_parent_child_2ph_1ph_load_no_issues():
    """2-phase line, 1-phase load — subset OK, no issues."""
    run_dss_script(SCRIPT_2PH_1PH_LOAD_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_parent_child_default_nodes_no_issues():
    """Load with bus1=B (default nodes) and 3-phase line — no issues."""
    run_dss_script(SCRIPT_DEFAULT_NODES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


# ---------------------------------------------------------------------------
# parent_child: mismatch cases
# ---------------------------------------------------------------------------


def test_parent_child_columns():
    """nodes_connections_parent_child_df always returns the expected columns."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert list(df.columns) == [
        "parent_name",
        "parent_bus",
        "parent_node",
        "element_name",
        "element_bus",
        "element_node",
    ]


def test_parent_child_empty_when_phases_match():
    """3-phase line and load at same bus produce no phase-connection issues."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_parent_child_detects_pd_mismatch():
    """2-phase line feeding 3-phase line is flagged."""
    run_dss_script(SCRIPT_PHASES_PD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    pd_issues = df[df["element_name"].str.startswith("line.")]
    assert len(pd_issues) >= 1
    assert "b" in pd_issues["parent_bus"].values or "b" in pd_issues["element_bus"].values


def test_parent_child_detects_load_mismatch():
    """Load with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_PHASES_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1
    assert load_issues.iloc[0]["element_name"] == "load.l"


def test_parent_child_2ph_3ph_load_flagged():
    """2-phase line, 3-phase load — load flagged."""
    run_dss_script(SCRIPT_2PH_3PH_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1
    assert load_issues.iloc[0]["element_name"] == "load.l"


def test_parent_child_1ph_2ph_load_flagged():
    """1-phase line, 2-phase load — load flagged."""
    run_dss_script(SCRIPT_1PH_2PH_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1


def test_parent_child_2ph_3ph_line_flagged():
    """2-phase line feeding 3-phase line — downstream line flagged."""
    run_dss_script(SCRIPT_2PH_3PH_LINE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    pd_issues = df[df["element_name"].str.startswith("line.")]
    assert len(pd_issues) >= 1
    assert "line.l2" in pd_issues["element_name"].values


def test_parent_child_detects_generator_mismatch():
    """Generator with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_GENERATOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    gen_issues = df[df["element_name"].str.startswith("generator.")]
    assert len(gen_issues) >= 1
    assert "generator.g1" in gen_issues["element_name"].values


def test_parent_child_detects_capacitor_mismatch():
    """Wye capacitor with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_CAPACITOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    cap_issues = df[df["element_name"].str.startswith("capacitor.")]
    assert len(cap_issues) >= 1
    assert "capacitor.c1" in cap_issues["element_name"].values


def test_parent_child_detects_delta_capacitor_mismatch():
    """Delta capacitor with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_DELTA_CAPACITOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    cap_issues = df[df["element_name"].str.startswith("capacitor.")]
    assert len(cap_issues) >= 1
    assert "capacitor.cdelta" in cap_issues["element_name"].values


def test_parent_child_parallel_transformers_no_false_positive():
    """3 single-phase transformers A->B provide phases 1,2,3 at B. 3-phase line B->C should NOT be flagged."""
    run_dss_script(SCRIPT_PARALLEL_1PH_XFMR_3PH_LINE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    pd_issues = df[df["element_name"].str.startswith("line.")]
    assert len(pd_issues) == 0


# ---------------------------------------------------------------------------
# propagated: OK and mismatch cases
# ---------------------------------------------------------------------------


def test_propagated_columns():
    """nodes_connections_propagated_df always returns the expected columns."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert list(df.columns) == [
        "parent_name",
        "parent_bus",
        "parent_node",
        "element_name",
        "element_bus",
        "element_node",
    ]


def test_propagated_empty_when_phases_match():
    """All phases match → empty DataFrame."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) == 0


def test_propagated_detects_first_mismatch_not_cascading():
    """line.l2 (3ph at B where only 2ph are validated) is flagged; downstream line.l3 and load.l are not."""
    run_dss_script(SCRIPT_PROPAGATED_NO_CASCADE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    flagged_names = set(df["element_name"])
    assert "line.l2" in flagged_names
    assert "line.l3" not in flagged_names
    assert "load.l" not in flagged_names
    line_l2_row = df[df["element_name"] == "line.l2"].iloc[0]
    assert line_l2_row["parent_name"] == "line.l1"


def test_propagated_detects_load_mismatch():
    """Load with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_PROPAGATED_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1
    assert load_issues.iloc[0]["element_name"] == "load.l"
    assert load_issues.iloc[0]["parent_name"] == "line.main"


def test_propagated_multi_branch():
    """Multi-branch scenario: only E (line.ce) and F (line.df) are flagged; H and G are not."""
    run_dss_script(SCRIPT_PROPAGATED_MULTI_BRANCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    flagged_names = set(df["element_name"])
    assert "line.ce" in flagged_names
    assert "line.df" in flagged_names
    assert "line.eh" not in flagged_names
    assert "line.fg" not in flagged_names
    assert "load.lh" not in flagged_names
    assert "load.lg" not in flagged_names


def test_propagated_1ph_source_ok():
    """1-phase source: propagated check uses correct source phases, no false flags."""
    run_dss_script(SCRIPT_1PH_SOURCE_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) == 0


def test_propagated_no_cascade():
    """Propagated check: L2 flagged; downstream L3 and load not cascaded."""
    run_dss_script(SCRIPT_PROPAGATED_NO_CASCADE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    flagged = set(df["element_name"])
    assert "line.l2" in flagged
    assert "line.l3" not in flagged
    assert "load.l" not in flagged


def test_propagated_detects_generator_mismatch():
    """Propagated check flags generator with phase mismatch."""
    run_dss_script(SCRIPT_GENERATOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) >= 1
    assert (df["element_name"].str.startswith("generator.")).any()


def test_propagated_detects_capacitor_mismatch():
    """Propagated check flags delta capacitor with phase mismatch."""
    run_dss_script(SCRIPT_DELTA_CAPACITOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    cap_issues = df[df["element_name"].str.startswith("capacitor.")]
    assert len(cap_issues) >= 1
    assert "capacitor.cdelta" in cap_issues["element_name"].values


def test_propagated_parallel_transformers_no_false_positive():
    """3 single-phase transformers A->B provide phases 1,2,3 at B. Propagated check should not flag B->C."""
    run_dss_script(SCRIPT_PARALLEL_1PH_XFMR_3PH_LINE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) == 0

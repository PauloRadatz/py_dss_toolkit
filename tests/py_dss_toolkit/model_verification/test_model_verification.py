# -*- coding: utf-8 -*-
"""
Unit tests for ModelVerification using DSS scripts as strings.
"""

import networkx as nx
import py_dss_interface

from py_dss_toolkit import dss_tools

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_EX_2 = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoTri phases=3 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800 leadlag=lead
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=delta
~ wdg=2 bus=B kv=0.22 kva=112.5 conn=wye
New load.l bus1=B kw=112.5 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_EX_3 = """
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
New load.l bus1=B kw=112.5 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

# Isolated branch: Line.Floating connects C-D with no path back to source
SCRIPT_ISOLATED_BRANCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l1 bus1=B kw=100 pf=1
New Line.Floating bus1=C bus2=D phases=3 r1=0.1 x1=0.1 c1=0 length=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# Isolated load: load.floating at bus C has no branch connecting it to source
SCRIPT_ISOLATED_LOAD = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.connected bus1=B kw=100 pf=1
New load.floating bus1=C kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# Disabled segment: Line.Off is enabled=no, should NOT appear in isolated_df
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

# Reversed case: Line has bus1=B bus2=A (DSS order opposite to BFS A->B)
SCRIPT_REVERSED_LINE = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=B bus2=A phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def run_dss_script(script: str):
    """Run DSS script string via dss.text() and return DSS instance."""
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())
    return dss


# ---------------------------------------------------------------------------
# same_buses_segments_df (moved from test_graph_builder.py)
# ---------------------------------------------------------------------------


def test_model_verification_same_buses_segments_df():
    """ex_3 has 3 transformers between A and B; all should appear in same_buses_segments_df."""
    run_dss_script(SCRIPT_EX_3)
    mv = dss_tools.model_verification
    same_buses = mv.same_buses_segments_df
    assert len(same_buses) == 3
    assert set(same_buses["name"]) == {"transformer.trafoa", "transformer.trafob", "transformer.trafoc"}
    assert (same_buses["segments_in_pair"] == 3).all()


def test_model_verification_same_buses_segments_df_empty_when_no_duplicates():
    """ex_2 has one element between A and B; same_buses_segments_df should be empty."""
    run_dss_script(SCRIPT_EX_2)
    mv = dss_tools.model_verification
    same_buses = mv.same_buses_segments_df
    assert len(same_buses) == 0


# ---------------------------------------------------------------------------
# isolated_df
# ---------------------------------------------------------------------------


def test_model_verification_isolated_df_columns():
    """isolated_df always returns a DataFrame with the expected columns."""
    run_dss_script(SCRIPT_EX_2)
    df = dss_tools.model_verification.isolated_df
    assert list(df.columns) == ["element_name", "bus1", "bus2", "type"]


def test_model_verification_isolated_df_empty_when_fully_connected():
    """All elements reachable from source → empty isolated_df."""
    run_dss_script(SCRIPT_EX_2)
    df = dss_tools.model_verification.isolated_df
    assert len(df) == 0


def test_model_verification_isolated_df_detects_isolated_branch():
    """Line with both endpoints unreachable from source appears as an isolated branch."""
    run_dss_script(SCRIPT_ISOLATED_BRANCH)
    df = dss_tools.model_verification.isolated_df
    assert len(df) == 1
    assert df.iloc[0]["element_name"] == "line.floating"
    assert df.iloc[0]["type"] == "branch"
    assert df.iloc[0]["bus1"] == "c"
    assert df.iloc[0]["bus2"] == "d"


def test_model_verification_isolated_df_detects_isolated_load():
    """Load whose bus has no path to source appears as an isolated load."""
    run_dss_script(SCRIPT_ISOLATED_LOAD)
    df = dss_tools.model_verification.isolated_df
    isolated_loads = df[df["type"] == "load"]
    assert len(isolated_loads) == 1
    assert isolated_loads.iloc[0]["element_name"] == "load.floating"
    assert isolated_loads.iloc[0]["bus1"] == "c"
    assert isolated_loads.iloc[0]["bus2"] == ""


def test_model_verification_isolated_df_disabled_not_reported():
    """Disabled segments are not energized but are not the same as isolated — they must not appear."""
    run_dss_script(SCRIPT_DISABLED_NOT_ISOLATED)
    df = dss_tools.model_verification.isolated_df
    assert len(df) == 0


# Two separate disconnected islands (C-D and E-F), neither reachable from source
SCRIPT_TWO_ISOLATED_ISLANDS = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.connected bus1=B kw=100 pf=1
New Line.Island1 bus1=C bus2=D phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.Island2 bus1=E bus2=F phases=3 r1=0.1 x1=0.1 c1=0 length=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# isolated_graph
# ---------------------------------------------------------------------------


def test_isolated_graph_returns_digraph():
    """isolated_graph is always a networkx DiGraph."""
    run_dss_script(SCRIPT_EX_2)
    G = dss_tools.model_verification.isolated_graph
    assert isinstance(G, nx.DiGraph)


def test_isolated_graph_empty_when_fully_connected():
    """Fully-connected circuit → isolated_graph has no nodes or edges."""
    run_dss_script(SCRIPT_EX_2)
    G = dss_tools.model_verification.isolated_graph
    assert G.number_of_nodes() == 0
    assert G.number_of_edges() == 0


def test_isolated_graph_contains_isolated_branch_edge():
    """Isolated branch appears as a directed edge with the segment name as attribute."""
    run_dss_script(SCRIPT_ISOLATED_BRANCH)
    G = dss_tools.model_verification.isolated_graph
    assert G.has_edge("c", "d")
    assert G.edges["c", "d"]["name"] == "line.floating"


def test_isolated_graph_isolated_branch_excludes_reachable_buses():
    """Buses reachable from source (a, b) must not appear in isolated_graph."""
    run_dss_script(SCRIPT_ISOLATED_BRANCH)
    G = dss_tools.model_verification.isolated_graph
    assert set(G.nodes()) == {"c", "d"}


def test_isolated_graph_contains_isolated_load_node():
    """Isolated load bus appears as a node with type='load_bus' and correct element_name."""
    run_dss_script(SCRIPT_ISOLATED_LOAD)
    G = dss_tools.model_verification.isolated_graph
    assert "c" in G.nodes()
    assert G.nodes["c"]["type"] == "load_bus"
    assert G.nodes["c"]["element_name"] == "load.floating"


def test_isolated_graph_load_excludes_reachable_buses():
    """Reachable buses (a, b) must not appear in isolated_graph for the isolated-load circuit."""
    run_dss_script(SCRIPT_ISOLATED_LOAD)
    G = dss_tools.model_verification.isolated_graph
    assert "a" not in G.nodes()
    assert "b" not in G.nodes()


def test_isolated_graph_consistent_with_isolated_df():
    """isolated_graph edges and load nodes must match the rows reported in isolated_df."""
    run_dss_script(SCRIPT_ISOLATED_BRANCH)
    mv = dss_tools.model_verification
    G = mv.isolated_graph
    df = mv.isolated_df
    branch_rows = df[df["type"] == "branch"]
    assert G.number_of_edges() == len(branch_rows)
    for _, row in branch_rows.iterrows():
        assert G.has_edge(row["bus1"], row["bus2"])


# ---------------------------------------------------------------------------
# isolated_subgraphs
# ---------------------------------------------------------------------------


def test_isolated_subgraphs_returns_list():
    """isolated_subgraphs is always a list."""
    run_dss_script(SCRIPT_EX_2)
    result = dss_tools.model_verification.isolated_subgraphs
    assert isinstance(result, list)


def test_isolated_subgraphs_empty_when_fully_connected():
    """Fully-connected circuit → isolated_subgraphs is an empty list."""
    run_dss_script(SCRIPT_EX_2)
    result = dss_tools.model_verification.isolated_subgraphs
    assert len(result) == 0


def test_isolated_subgraphs_one_island_for_isolated_branch():
    """Single isolated branch → one subgraph with 2 nodes and 1 edge."""
    run_dss_script(SCRIPT_ISOLATED_BRANCH)
    result = dss_tools.model_verification.isolated_subgraphs
    assert len(result) == 1
    sg = result[0]
    assert isinstance(sg, nx.DiGraph)
    assert sg.number_of_nodes() == 2
    assert sg.number_of_edges() == 1


def test_isolated_subgraphs_one_island_for_isolated_load():
    """Single isolated load bus → one subgraph with 1 node and no edges."""
    run_dss_script(SCRIPT_ISOLATED_LOAD)
    result = dss_tools.model_verification.isolated_subgraphs
    assert len(result) == 1
    sg = result[0]
    assert sg.number_of_nodes() == 1
    assert sg.number_of_edges() == 0


def test_isolated_subgraphs_two_islands():
    """Two disconnected isolated branches → two separate subgraphs."""
    run_dss_script(SCRIPT_TWO_ISOLATED_ISLANDS)
    result = dss_tools.model_verification.isolated_subgraphs
    assert len(result) == 2
    all_nodes = set()
    for sg in result:
        assert sg.number_of_nodes() == 2
        assert sg.number_of_edges() == 1
        all_nodes.update(sg.nodes())
    assert all_nodes == {"c", "d", "e", "f"}


def test_isolated_subgraphs_nodes_partition_isolated_graph():
    """Node sets of all subgraphs together equal the full isolated_graph node set."""
    run_dss_script(SCRIPT_TWO_ISOLATED_ISLANDS)
    mv = dss_tools.model_verification
    G = mv.isolated_graph
    subgraph_nodes = set().union(*(set(sg.nodes()) for sg in mv.isolated_subgraphs))
    assert subgraph_nodes == set(G.nodes())


# ---------------------------------------------------------------------------
# reversed_segments_df (via model_verification)
# ---------------------------------------------------------------------------


def test_model_verification_reversed_segments_df_filters_graph_df():
    """model_verification.reversed_segments_df filters graph_df for reversed edges."""
    run_dss_script(SCRIPT_REVERSED_LINE)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    model = dss_tools.model
    mv_df = mv.reversed_segments_df
    expected = model.graph_df[model.graph_df["reversed"]].reset_index(drop=True)
    assert mv_df.equals(expected)


def test_model_verification_reversed_segments_df_has_reversed_true():
    """Reversed line should show up with reversed=True in model_verification.reversed_segments_df."""
    run_dss_script(SCRIPT_REVERSED_LINE)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = mv.reversed_segments_df
    assert len(df) >= 1
    assert (df["reversed"]).all()


def test_model_verification_reversed_segments_df_13bus(dss_tools_13bus):
    """reversed_segments_df via model_verification filters graph_df on the 13-bus feeder."""
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    model = dss_tools.model
    expected = model.graph_df[model.graph_df["reversed"]].reset_index(drop=True)
    assert mv.reversed_segments_df.equals(expected)


# ---------------------------------------------------------------------------
# loads_transformer_voltage_df
# ---------------------------------------------------------------------------

# 3-phase delta/wye transformer, secondary kv=0.22.
# Load at B.1.2.3 → phase_count=3 → expects vll=0.22.
SCRIPT_3PH_LOAD_CORRECT_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=3 windings=2 xhl=3
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=delta
~ wdg=2 bus=B kv=0.22 kva=112.5 conn=wye
New load.l3ok bus1=B.1.2.3 kv=0.22 phases=3 kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

# Same circuit but load kv deliberately set to vln (0.13) instead of vll (0.22).
SCRIPT_3PH_LOAD_WRONG_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=3 windings=2 xhl=3
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=delta
~ wdg=2 bus=B kv=0.22 kva=112.5 conn=wye
New load.l3bad bus1=B.1.2.3 kv=0.13 phases=3 kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

# 1-phase transformer, secondary kv=0.127 wye (LN connection: B.1 has one phase node).
# Load at B.1 → phase_count=1 → expects vln ≈ 0.127 (rounds to 0.13).
SCRIPT_1PH_LN_LOAD_CORRECT_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=1 windings=2 xhl=3
~ wdg=1 bus=A.1.2 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.1 kv=0.127 kva=37.5 conn=wye
New load.l1ok bus1=B.1 kv=0.127 phases=1 kw=37.5 pf=1
Set voltagebases=[13.8 0.127]
Calcvoltagebases
Solve
"""

# Same 1-phase LN circuit but load kv set to 0.22 (vll) instead of vln.
SCRIPT_1PH_LN_LOAD_WRONG_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=1 windings=2 xhl=3
~ wdg=1 bus=A.1.2 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.1 kv=0.127 kva=37.5 conn=wye
New load.l1bad bus1=B.1 kv=0.22 phases=1 kw=37.5 pf=1
Set voltagebases=[13.8 0.127]
Calcvoltagebases
Solve
"""


def test_loads_transformer_voltage_df_columns():
    """Property always returns a DataFrame with the expected columns."""
    run_dss_script(SCRIPT_3PH_LOAD_CORRECT_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert list(df.columns) == ["Load", "kV_set", "kV_use"]


def test_loads_transformer_voltage_df_empty_when_3ph_kv_correct():
    """3-phase load whose kv matches the transformer vll produces an empty result."""
    run_dss_script(SCRIPT_3PH_LOAD_CORRECT_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 0


def test_loads_transformer_voltage_df_detects_3ph_kv_mismatch():
    """3-phase load with kv set to vln instead of vll is flagged."""
    run_dss_script(SCRIPT_3PH_LOAD_WRONG_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 1
    assert df.iloc[0]["Load"] == "l3bad"
    assert round(df.iloc[0]["kV_set"], 2) == 0.13
    assert round(df.iloc[0]["kV_use"], 2) == 0.22


def test_loads_transformer_voltage_df_empty_when_1ph_ln_kv_correct():
    """1-phase LN load whose kv matches the transformer vln produces an empty result."""
    run_dss_script(SCRIPT_1PH_LN_LOAD_CORRECT_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 0


def test_loads_transformer_voltage_df_detects_1ph_ln_kv_mismatch():
    """1-phase LN load with kv set to vll instead of vln is flagged."""
    run_dss_script(SCRIPT_1PH_LN_LOAD_WRONG_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 1
    assert df.iloc[0]["Load"] == "l1bad"
    assert round(df.iloc[0]["kV_set"], 2) == 0.22
    assert round(df.iloc[0]["kV_use"], 2) == 0.13


# ---------------------------------------------------------------------------
# nodes_connections_parent_child_df  (renamed from phases_connections_df)
# ---------------------------------------------------------------------------

# Simple 3-phase radial: Line A-B 3ph, Load at B 3ph. All phases match.
SCRIPT_PHASES_OK = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

# 2-phase line A-B feeds 3-phase line B-C. At B, downstream has phase 3 that upstream lacks.
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

# 2-phase line A-B, 3-phase load at B. Load has phase 3 that line does not provide.
SCRIPT_PHASES_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2.3 phases=3 kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_nodes_connections_parent_child_df_columns():
    """nodes_connections_parent_child_df always returns a DataFrame with the expected columns."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert list(df.columns) == [
        "parent_name", "parent_bus", "parent_node",
        "element_name", "element_bus", "element_node",
    ]


def test_nodes_connections_parent_child_df_empty_when_phases_match():
    """3-phase line and load at same bus produce no phase-connection issues."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) == 0


def test_nodes_connections_parent_child_df_detects_pd_mismatch():
    """2-phase line feeding 3-phase line is flagged (downstream has phase 3 upstream lacks)."""
    run_dss_script(SCRIPT_PHASES_PD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    pd_issues = df[df["element_name"].str.startswith("line.")]
    assert len(pd_issues) >= 1
    assert "b" in pd_issues["parent_bus"].values or "b" in pd_issues["element_bus"].values


def test_nodes_connections_parent_child_df_detects_load_mismatch():
    """Load with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_PHASES_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    assert len(df) >= 1
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1
    assert load_issues.iloc[0]["element_name"] == "load.l"


# ---------------------------------------------------------------------------
# nodes_connections_propagated_df
# ---------------------------------------------------------------------------

# Multi-branch topology for propagated check:
#   A(ABC) -> B(ABC) -> C(AB) -> E(ABC)*  -> H(A)
#                     -> D(A)  -> F(B)*    -> G(A)
# Only E and F should be flagged; H and G should NOT be flagged.
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

# Propagated check with a load mismatch: 2-phase line A-B, 3-phase load at B.
SCRIPT_PROPAGATED_LOAD_MISMATCH = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.Main phases=2 bus1=A.1.2 bus2=B.1.2 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1.2.3 phases=3 kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_nodes_connections_propagated_df_columns():
    """nodes_connections_propagated_df always returns the expected columns."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert list(df.columns) == [
        "parent_name", "parent_bus", "parent_node",
        "element_name", "element_bus", "element_node",
    ]


def test_nodes_connections_propagated_df_empty_when_phases_match():
    """All phases match → empty DataFrame."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) == 0


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


def test_nodes_connections_propagated_df_detects_first_mismatch_not_cascading():
    """line.l2 (3ph at B where only 2ph are validated) is flagged; downstream line.l3 and load.l are not."""
    run_dss_script(SCRIPT_PROPAGATED_NO_CASCADE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    flagged_names = set(df["element_name"])
    assert "line.l2" in flagged_names
    assert "line.l3" not in flagged_names
    assert "load.l" not in flagged_names


def test_nodes_connections_propagated_df_detects_load_mismatch():
    """Load with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_PROPAGATED_LOAD_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    load_issues = df[df["element_name"].str.startswith("load.")]
    assert len(load_issues) >= 1
    assert load_issues.iloc[0]["element_name"] == "load.l"


def test_nodes_connections_propagated_df_multi_branch():
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


# ---------------------------------------------------------------------------
# Source phases (1-phase source uses actual phases)
# ---------------------------------------------------------------------------

SCRIPT_1PH_SOURCE_OK = """
ClearAll
New Circuit.Thevenin bus1=A.1 pu=1.0 basekv=0.127 phases=1 model=ideal
New Line.Main phases=1 bus1=A.1 bus2=B.1 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B.1 phases=1 kw=10 pf=1
Set voltagebases=[0.127]
Calcvoltagebases
Solve
"""


def test_nodes_connections_propagated_df_1ph_source_ok():
    """1-phase source: propagated check uses correct source phases, no false flags."""
    run_dss_script(SCRIPT_1PH_SOURCE_OK)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) == 0


# ---------------------------------------------------------------------------
# meshed_edges_df / is_radial
# ---------------------------------------------------------------------------

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


def test_meshed_edges_df_radial_empty():
    """Radial circuit has empty meshed_edges_df and is_radial=True."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    assert mv.is_radial is True
    assert len(mv.meshed_edges_df) == 0


def test_meshed_edges_df_meshed_has_edges():
    """Meshed circuit (A-B-C-A loop) has loop-closing segments."""
    run_dss_script(SCRIPT_MESHED_LOOP)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    assert mv.is_radial is False
    df = mv.meshed_edges_df
    assert len(df) >= 1
    assert list(df.columns) == ["bus1", "bus2", "name", "type"]
    assert set(df["name"]) >= {"line.l1", "line.l2", "line.l3"}


def test_is_radial_property():
    """is_radial is True for radial, False for meshed."""
    run_dss_script(SCRIPT_PHASES_OK)
    dss_tools.model.refresh_graph()
    assert dss_tools.model_verification.is_radial is True
    run_dss_script(SCRIPT_MESHED_LOOP)
    dss_tools.model.refresh_graph()
    assert dss_tools.model_verification.is_radial is False


# ---------------------------------------------------------------------------
# disabled_segments_df
# ---------------------------------------------------------------------------


def test_disabled_segments_df_returns_disabled_only():
    """disabled_segments_df returns only segments with enabled=False."""
    run_dss_script(SCRIPT_DISABLED_NOT_ISOLATED)
    df = dss_tools.model.disabled_segments_df
    assert len(df) >= 1
    assert "line.off" in df["name"].str.lower().values


def test_disabled_segments_df_empty_when_all_enabled():
    """disabled_segments_df is empty when all segments are enabled."""
    run_dss_script(SCRIPT_PHASES_OK)
    df = dss_tools.model.disabled_segments_df
    assert not df


# ---------------------------------------------------------------------------
# Additional edge-case tests
# ---------------------------------------------------------------------------

SCRIPT_NO_REVERSED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_NO_LOADS = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kV=13.8 kva=300 conn=delta
~ wdg=2 bus=B kV=0.22  kva=300 conn=wye
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""


def test_reversed_segments_df_no_reversed_returns_empty():
    """When DSS order matches BFS order, reversed_segments_df is empty."""
    run_dss_script(SCRIPT_NO_REVERSED)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = mv.reversed_segments_df
    assert len(df) == 0


def test_loads_transformer_voltage_df_no_loads_returns_empty():
    """Circuit with transformer but no loads: loads_transformer_voltage_df is empty."""
    run_dss_script(SCRIPT_NO_LOADS)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = mv.loads_transformer_voltage_df
    assert len(df) == 0


# ---------------------------------------------------------------------------
# Parallel single-phase transformers: parent-child and propagated checks
# ---------------------------------------------------------------------------

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


def test_nodes_connections_parent_child_parallel_transformers_no_false_positive():
    """3 single-phase transformers A->B provide phases 1,2,3 at B.

    A 3-phase line B->C should NOT be flagged as a phase issue.
    """
    run_dss_script(SCRIPT_PARALLEL_1PH_XFMR_3PH_LINE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    pd_issues = df[df["element_name"].str.startswith("line.")]
    assert len(pd_issues) == 0


def test_nodes_connections_propagated_parallel_transformers_no_false_positive():
    """3 single-phase transformers A->B provide phases 1,2,3 at B.

    Propagated check should see validated phases {1,2,3} at B.
    A 3-phase line B->C and load at C should NOT be flagged.
    """
    run_dss_script(SCRIPT_PARALLEL_1PH_XFMR_3PH_LINE)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) == 0


# ---------------------------------------------------------------------------
# PC elements: generator and capacitor phase checks
# ---------------------------------------------------------------------------

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


def test_nodes_connections_parent_child_detects_generator_mismatch():
    """Generator with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_GENERATOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    gen_issues = df[df["element_name"].str.startswith("generator.")]
    assert len(gen_issues) >= 1
    assert "generator.g1" in gen_issues["element_name"].values


def test_nodes_connections_parent_child_detects_capacitor_mismatch():
    """Capacitor with 3 phases at bus fed by 2-phase line is flagged."""
    run_dss_script(SCRIPT_CAPACITOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_parent_child_df
    cap_issues = df[df["element_name"].str.startswith("capacitor.")]
    assert len(cap_issues) >= 1
    assert "capacitor.c1" in cap_issues["element_name"].values


def test_nodes_connections_propagated_detects_generator_mismatch():
    """Propagated check flags generator with phase mismatch."""
    run_dss_script(SCRIPT_GENERATOR_PHASE_MISMATCH)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.nodes_connections_propagated_df
    assert len(df) >= 1
    assert (df["element_name"].str.startswith("generator.")).any()


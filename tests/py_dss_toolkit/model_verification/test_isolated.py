# -*- coding: utf-8 -*-
"""Tests for isolated_df, isolated_graph, and isolated_subgraphs."""

import networkx as nx

from py_dss_toolkit import dss_tools

from .helpers import run_dss_script

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_FULLY_CONNECTED = """
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

SCRIPT_ISOLATED_DELTA_CAPACITOR = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=B kw=100 pf=1
New Line.L2 bus1=C bus2=D phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Capacitor.Cdelta bus1=C phases=3 kvar=50 conn=delta
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# isolated_df
# ---------------------------------------------------------------------------


def test_isolated_df_columns():
    """isolated_df always returns a DataFrame with the expected columns."""
    run_dss_script(SCRIPT_FULLY_CONNECTED)
    df = dss_tools.model_verification.isolated_df
    assert list(df.columns) == ["element_name", "bus1", "bus2", "type"]


def test_isolated_df_empty_when_fully_connected():
    """All elements reachable from source → empty isolated_df."""
    run_dss_script(SCRIPT_FULLY_CONNECTED)
    df = dss_tools.model_verification.isolated_df
    assert len(df) == 0


def test_isolated_df_detects_isolated_branch():
    """Line with both endpoints unreachable from source appears as an isolated segment."""
    run_dss_script(SCRIPT_ISOLATED_BRANCH)
    df = dss_tools.model_verification.isolated_df
    assert len(df) == 1
    assert df.iloc[0]["element_name"] == "line.floating"
    assert df.iloc[0]["type"] == "segment"
    assert df.iloc[0]["bus1"] == "c"
    assert df.iloc[0]["bus2"] == "d"


def test_isolated_df_detects_isolated_load():
    """Load whose bus has no path to source appears as an isolated shunt element."""
    run_dss_script(SCRIPT_ISOLATED_LOAD)
    df = dss_tools.model_verification.isolated_df
    isolated_shunts = df[df["type"] == "shunt"]
    assert len(isolated_shunts) == 1
    assert isolated_shunts.iloc[0]["element_name"] == "load.floating"
    assert isolated_shunts.iloc[0]["bus1"] == "c"
    assert isolated_shunts.iloc[0]["bus2"] == ""


def test_isolated_df_disabled_not_reported():
    """Disabled segments are not energized but are not the same as isolated — they must not appear."""
    run_dss_script(SCRIPT_DISABLED_NOT_ISOLATED)
    df = dss_tools.model_verification.isolated_df
    assert len(df) == 0


def test_isolated_df_includes_delta_capacitor():
    """Isolated delta capacitor at bus C appears in isolated_df as shunt element."""
    run_dss_script(SCRIPT_ISOLATED_DELTA_CAPACITOR)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.isolated_df
    shunt_rows = df[df["type"] == "shunt"]
    cap_rows = shunt_rows[shunt_rows["element_name"].str.startswith("capacitor.")]
    assert len(cap_rows) >= 1
    assert "capacitor.cdelta" in cap_rows["element_name"].values


# ---------------------------------------------------------------------------
# isolated_graph
# ---------------------------------------------------------------------------


def test_isolated_graph_returns_digraph():
    """isolated_graph is always a networkx DiGraph."""
    run_dss_script(SCRIPT_FULLY_CONNECTED)
    G = dss_tools.model_verification.isolated_graph
    assert isinstance(G, nx.DiGraph)


def test_isolated_graph_empty_when_fully_connected():
    """Fully-connected circuit → isolated_graph has no nodes or edges."""
    run_dss_script(SCRIPT_FULLY_CONNECTED)
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
    """Isolated load bus appears as a node with shunt_elements containing the load."""
    run_dss_script(SCRIPT_ISOLATED_LOAD)
    G = dss_tools.model_verification.isolated_graph
    assert "c" in G.nodes()
    assert G.nodes["c"]["shunt_elements"] == [("load.floating", "load")]


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
    segment_rows = df[df["type"] == "segment"]
    assert G.number_of_edges() == len(segment_rows)
    for _, row in segment_rows.iterrows():
        assert G.has_edge(row["bus1"], row["bus2"])


# ---------------------------------------------------------------------------
# isolated_subgraphs
# ---------------------------------------------------------------------------


def test_isolated_subgraphs_returns_list():
    """isolated_subgraphs is always a list."""
    run_dss_script(SCRIPT_FULLY_CONNECTED)
    result = dss_tools.model_verification.isolated_subgraphs
    assert isinstance(result, list)


def test_isolated_subgraphs_empty_when_fully_connected():
    """Fully-connected circuit → isolated_subgraphs is an empty list."""
    run_dss_script(SCRIPT_FULLY_CONNECTED)
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

# -*- coding: utf-8 -*-
"""
Unit tests for GraphBuilder using DSS scripts as strings.
Scripts are based on examples from RadatzAcademyBR module_4.
No show or export commands; dump lines stripped.
"""

import py_dss_interface

from py_dss_toolkit import dss_tools
from py_dss_toolkit.graph.GraphBuilder import GraphBuilder

# ---------------------------------------------------------------------------
# DSS Scripts (from module_4, cleaned: no dump/show/export)
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

SCRIPT_12_3PH_DY_11 = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoTri phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kV=13.8 kva=300 conn=delta
~ wdg=2 bus=B kV=0.22 kva=300 conn=wye
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_11_3PH_DD = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoTri phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kv=13.8 kva=300 conn=delta
~ wdg=2 bus=B kv=0.22 kva=300 conn=delta
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_8_3PH_YY_GR = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoTri phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kv=13.8 kva=300 conn=wye
~ wdg=2 bus=B kv=0.22 kva=300 conn=wye
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_6_1PH_LN_LN = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoMono phases=1 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A.2 kv=7.9674 kva=100
~ wdg=2 bus=B.2 kv=0.12702 kva=100
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_7_1PH_LL_LL = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoMono phases=1 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A.1.2 kv=13.8 kva=100
~ wdg=2 bus=B.1.2 kv=0.22 kva=100
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_EX_1 = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoTri phases=3 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=wye
~ wdg=2 bus=B.1.2.3.4 kv=0.22 kva=112.5 conn=wye
new reactor.g phases=1 bus1=B.4 bus2=B.0 r=10 x=0
Set voltagebases=[13.8 0.22]
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

# Chain A->B->C: 2 edges
SCRIPT_CHAIN_AB_BC = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=C kw=100 pf=1
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
    dss.text(script.strip())
    return dss


# ---------------------------------------------------------------------------
# 1. Source bus and basic structure
# ---------------------------------------------------------------------------


def test_graph_builder_source_bus():
    dss = run_dss_script(SCRIPT_EX_2)
    G = GraphBuilder.build(dss)
    assert G.graph["source_bus"] == "a"


def test_graph_builder_nodes():
    dss = run_dss_script(SCRIPT_EX_2)
    G = GraphBuilder.build(dss)
    assert set(G.nodes()) == {"a", "b"}


# ---------------------------------------------------------------------------
# 2. Edge count and direction
# ---------------------------------------------------------------------------


def test_graph_builder_edge_count():
    dss_chain = run_dss_script(SCRIPT_CHAIN_AB_BC)
    G_chain = GraphBuilder.build(dss_chain)
    dss_ex2 = run_dss_script(SCRIPT_EX_2)
    G_ex2 = GraphBuilder.build(dss_ex2)
    assert G_ex2.number_of_edges() == 1
    assert G_chain.number_of_edges() == 2


def test_graph_builder_edge_direction_away_from_source():
    dss = run_dss_script(SCRIPT_EX_2)
    G = GraphBuilder.build(dss)
    source = G.graph["source_bus"]
    for u, v in G.edges():
        assert u == source or G.has_edge(source, u)
    assert list(G.edges()) == [("a", "b")]


# ---------------------------------------------------------------------------
# 3. Reversed flag
# ---------------------------------------------------------------------------


def test_graph_builder_reversed_flag_when_dss_order_matches_bfs():
    dss = run_dss_script(SCRIPT_EX_2)
    G = GraphBuilder.build(dss)
    # DSS: bus1=A, bus2=B; BFS A->B, so no swap
    edges = list(G.edges(data=True))
    _, _, attrs = edges[0]
    assert attrs["reversed"] is False


def test_graph_builder_reversed_flag_when_dss_order_flipped():
    dss = run_dss_script(SCRIPT_REVERSED_LINE)
    G = GraphBuilder.build(dss)
    # DSS: bus1=B, bus2=A; BFS from A discovers B, adds A->B with swap
    edges = list(G.edges(data=True))
    _, _, attrs = edges[0]
    assert attrs["reversed"] is True


# ---------------------------------------------------------------------------
# 4. Transformer enrichment
# ---------------------------------------------------------------------------


def test_graph_builder_transformer_has_kv_conn_attrs():
    dss = run_dss_script(SCRIPT_12_3PH_DY_11)
    G = GraphBuilder.build(dss)
    edges = list(G.edges(data=True))
    _, _, attrs = edges[0]
    assert "kv_primary" in attrs
    assert "kv_secondary" in attrs
    assert "conn_primary" in attrs
    assert "conn_secondary" in attrs
    assert attrs["kv_primary"] == 13.8
    assert attrs["kv_secondary"] == 0.22
    assert attrs["conn_primary"] == "delta"
    assert attrs["conn_secondary"] == "wye"


# ---------------------------------------------------------------------------
# 5. Multiphase (nodes1, nodes2)
# ---------------------------------------------------------------------------


def test_graph_builder_1ph_has_correct_nodes():
    dss = run_dss_script(SCRIPT_6_1PH_LN_LN)
    G = GraphBuilder.build(dss)
    edges = list(G.edges(data=True))
    _, _, attrs = edges[0]
    assert attrs["phases"] == 1
    assert len(attrs["nodes1"]) == 1
    assert len(attrs["nodes2"]) == 1


def test_graph_builder_3ph_has_three_phases():
    dss = run_dss_script(SCRIPT_12_3PH_DY_11)
    G = GraphBuilder.build(dss)
    edges = list(G.edges(data=True))
    _, _, attrs = edges[0]
    assert attrs["phases"] == 3


# ---------------------------------------------------------------------------
# 6. CircuitGraph integration
# ---------------------------------------------------------------------------


def test_circuit_graph_reversed_segments_df():
    run_dss_script(SCRIPT_REVERSED_LINE)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = dss_tools.model.graph_df
    assert "reversed" in df.columns
    reversed_df = mv.reversed_segments_df
    assert len(reversed_df) >= 1
    assert (reversed_df["reversed"]).all()
    assert reversed_df.equals(df[df["reversed"]].reset_index(drop=True))


# ---------------------------------------------------------------------------
# 7. 13-bus IEEE model (complex)
# ---------------------------------------------------------------------------


def test_graph_builder_13bus_source_bus(dss_tools_13bus):
    G = GraphBuilder.build(dss_tools_13bus)
    assert G.graph["source_bus"] == "sourcebus"


def test_graph_builder_13bus_has_expected_structure(dss_tools_13bus):
    G = GraphBuilder.build(dss_tools_13bus)
    assert G.number_of_nodes() >= 10
    assert G.number_of_edges() >= 5
    source = G.graph["source_bus"]
    assert source in G.nodes()
    for _, _, attrs in G.edges(data=True):
        assert "reversed" in attrs


def test_graph_builder_13bus_graph_df_reversed_column(dss_tools_13bus):
    model = dss_tools.model
    model.refresh_graph()
    df = model.graph_df
    assert "reversed" in df.columns
    assert len(df) >= 5


def test_graph_builder_13bus_reversed_segments_df(dss_tools_13bus):
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = dss_tools.model.graph_df
    reversed_df = mv.reversed_segments_df
    assert (reversed_df["reversed"]).all()
    assert reversed_df.equals(df[df["reversed"]].reset_index(drop=True))


def test_graph_builder_13bus_edit_line_reverses_order_shows_reversed(dss_tools_13bus):
    """Edit Line.632633 to swap bus1/bus2, then verify the edge is marked reversed."""
    dss_tools.text("edit line.632633 bus1=633 bus2=632")
    dss_tools.text("solve")
    model = dss_tools.model
    model.refresh_graph()
    df = model.graph_df
    line_632633 = df[df["name"] == "line.632633"]
    assert len(line_632633) == 1
    assert line_632633["reversed"].iloc[0]


def test_graph_builder_13bus_edit_transformer_wdg_order_shows_reversed(dss_tools_13bus):
    """Edit Transformer.Sub to swap wdg=1/wdg=2, then verify the edge is marked reversed."""
    dss_tools.text("edit Transformer.Sub wdg=2 bus=SourceBus   conn=delta  kv=115 wdg=1 bus=650   conn=wye    kv=4.16")
    dss_tools.text("solve")
    model = dss_tools.model
    model.refresh_graph()
    df = model.graph_df
    tr_sub = df[df["name"] == "transformer.sub"]
    assert len(tr_sub) == 1
    assert tr_sub["reversed"].iloc[0]


# ---------------------------------------------------------------------------
# 8. Parallel single-phase transformers (MultiDiGraph)
# ---------------------------------------------------------------------------


def test_graph_builder_parallel_single_phase_transformers_edge_count():
    """3 single-phase transformers between A and B: graph has 3 edges."""
    dss = run_dss_script(SCRIPT_EX_3)
    G = GraphBuilder.build(dss)
    assert G.number_of_edges() == 3
    assert set(G.nodes()) == {"a", "b"}


def test_graph_builder_parallel_single_phase_transformers_each_has_correct_nodes():
    """Each of the 3 parallel transformers has its own nodes1/nodes2."""
    dss = run_dss_script(SCRIPT_EX_3)
    G = GraphBuilder.build(dss)
    edges = {key: data for _, _, key, data in G.edges(data=True, keys=True)}
    assert len(edges) == 3
    assert "transformer.trafoa" in edges
    assert "transformer.trafob" in edges
    assert "transformer.trafoc" in edges
    nodes2_sets = [set(_str_list(edges[k]["nodes2"])) for k in sorted(edges)]
    all_phases = set()
    for s in nodes2_sets:
        all_phases |= s
    assert all_phases == {"1", "2", "3"}


def test_graph_builder_parallel_transformers_graph_df_has_all():
    """graph_df includes all 3 parallel transformers."""
    run_dss_script(SCRIPT_EX_3)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.graph_df
    trafos = df[df["type"] == "transformer"]
    assert len(trafos) == 3
    names = set(trafos["name"])
    assert names == {"transformer.trafoa", "transformer.trafob", "transformer.trafoc"}


def _str_list(lst):
    return [str(x) for x in lst]

# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd

import networkx as nx

from py_dss_toolkit.model.ModelBase import ModelBase


def _cycle_edges_with_levels(G: nx.Graph) -> list[tuple[frozenset, int, int]]:
    """For each cycle, return (bus_pair, cycle_id, level) for edges in order.

    cycle_id starts at 1. level starts at 1 and increments around the loop.
    """
    result: list[tuple[frozenset, int, int]] = []
    try:
        basis = nx.cycle_basis(G)
    except nx.NetworkXNoCycle:
        return result

    for cycle_id, nodes in enumerate(basis, start=1):
        if len(nodes) < 2:
            continue
        sub = G.subgraph(nodes)
        try:
            cycle_edges = nx.find_cycle(sub)
        except nx.NetworkXNoCycle:
            continue
        for level, (u, v) in enumerate(cycle_edges, start=1):
            pair = frozenset((u, v))
            result.append((pair, cycle_id, level))

    return result


class LoopEdgesDF:
    """Segments that are part of loops (meshed topology).

    Builds an undirected graph from all enabled segments. Edges that are not
    bridges (i.e. part of at least one cycle) are reported. Radial circuits
    have an empty loop_edges_df.

    When meshed, each row includes cycle_id (1, 2, ...) and level (1, 2, ...)
    indicating the edge's position going around that cycle. An edge in multiple
    cycles appears multiple times (one row per cycle).
    """

    def __init__(self, model: ModelBase):
        self._model = model

    @property
    def loop_edges_df(self) -> pd.DataFrame:
        """DataFrame of segments that close loops (bus1, bus2, name, type, cycle_id, level)."""
        return self._build_loop_edges_df()

    @property
    def is_radial(self) -> bool:
        """True if the circuit has no loops (all segments form a forest)."""
        return len(self.loop_edges_df) == 0

    def _build_loop_edges_df(self) -> pd.DataFrame:
        segments = self._model.segments_df
        enabled = segments[segments["enabled"]].copy()
        enabled["bus1"] = enabled["bus1"].str.lower()
        enabled["bus2"] = enabled["bus2"].str.lower()
        enabled = enabled[enabled["bus1"] != enabled["bus2"]]

        if enabled.empty:
            return pd.DataFrame(columns=["bus1", "bus2", "name", "type", "cycle_id", "level"])

        G = nx.Graph()
        for _, row in enabled.iterrows():
            G.add_edge(row["bus1"], row["bus2"])

        bridges = set()
        for u, v in nx.bridges(G):
            bridges.add(frozenset((u, v)))

        pair_levels: dict[frozenset, list[tuple[int, int]]] = {}
        for pair, cycle_id, level in _cycle_edges_with_levels(G):
            if pair not in bridges:
                pair_levels.setdefault(pair, []).append((cycle_id, level))

        rows = []
        for _, row in enabled.iterrows():
            pair = frozenset((row["bus1"], row["bus2"]))
            if pair not in bridges:
                levels = pair_levels.get(pair, [(1, 1)])
                for cycle_id, level in levels:
                    rows.append({
                        "bus1": row["bus1"],
                        "bus2": row["bus2"],
                        "name": row["name"],
                        "type": row["type"],
                        "cycle_id": cycle_id,
                        "level": level,
                    })

        return pd.DataFrame(rows, columns=["bus1", "bus2", "name", "type", "cycle_id", "level"])

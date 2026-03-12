# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd

import networkx as nx

from py_dss_toolkit.model.ModelBase import ModelBase


class MeshedEdgesDF:
    """Segments that are part of loops (meshed topology).

    Builds an undirected graph from all enabled segments. Edges that are not
    bridges (i.e. part of at least one cycle) are reported. Radial circuits
    have an empty meshed_edges_df.
    """

    def __init__(self, model: ModelBase):
        self._model = model

    @property
    def meshed_edges_df(self) -> pd.DataFrame:
        """DataFrame of segments that close loops (bus1, bus2, name, type)."""
        return self._build_meshed_edges_df()

    @property
    def is_radial(self) -> bool:
        """True if the circuit has no loops (all segments form a forest)."""
        return len(self.meshed_edges_df) == 0

    def _build_meshed_edges_df(self) -> pd.DataFrame:
        segments = self._model.segments_df
        enabled = segments[segments["enabled"]].copy()
        enabled["bus1"] = enabled["bus1"].str.lower()
        enabled["bus2"] = enabled["bus2"].str.lower()
        enabled = enabled[enabled["bus1"] != enabled["bus2"]]

        if enabled.empty:
            return pd.DataFrame(columns=["bus1", "bus2", "name", "type"])

        G = nx.Graph()
        for _, row in enabled.iterrows():
            G.add_edge(row["bus1"], row["bus2"])

        bridges = set()
        for u, v in nx.bridges(G):
            bridges.add(frozenset((u, v)))

        rows = []
        for _, row in enabled.iterrows():
            pair = frozenset((row["bus1"], row["bus2"]))
            if pair not in bridges:
                rows.append({
                    "bus1": row["bus1"],
                    "bus2": row["bus2"],
                    "name": row["name"],
                    "type": row["type"],
                })

        return pd.DataFrame(rows, columns=["bus1", "bus2", "name", "type"])

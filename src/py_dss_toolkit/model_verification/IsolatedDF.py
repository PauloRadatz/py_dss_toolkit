# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import List

import networkx as nx
import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.ModelBase import ModelBase


class IsolatedDF:

    def __init__(self, dss: DSS, model: ModelBase):
        self._dss = dss
        self._model = model

    @property
    def isolated_df(self) -> pd.DataFrame:
        """DataFrame of enabled branches and loads not reachable from the source bus."""
        G = self.isolated_graph
        data = []

        for u, v, attrs in G.edges(data=True):
            data.append({
                "element_name": attrs.get("name", ""),
                "bus1": u,
                "bus2": v,
                "type": "branch",
            })

        for node, attrs in G.nodes(data=True):
            if attrs.get("type") == "load_bus":
                data.append({
                    "element_name": attrs.get("element_name", ""),
                    "bus1": node,
                    "bus2": "",
                    "type": "load",
                })

        return pd.DataFrame(data, columns=["element_name", "bus1", "bus2", "type"])

    @property
    def isolated_graph(self) -> nx.DiGraph:
        """DiGraph of all buses and enabled branches not reachable from the source bus.

        Nodes that come exclusively from loads (no branch endpoint) carry
        ``type="load_bus"`` and ``element_name="load.<name>"`` as node attributes.
        Edge attributes mirror the segment data: ``name``, ``type``.
        """
        return self._build_isolated_graph()

    @property
    def isolated_subgraphs(self) -> List[nx.DiGraph]:
        """One DiGraph per weakly-connected isolated island.

        Useful for analysing or visualising each disconnected component
        independently (e.g. to count elements per island or layout each one).
        """
        G = self.isolated_graph
        return [
            G.subgraph(component).copy()
            for component in nx.weakly_connected_components(G)
        ]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_isolated_graph(self) -> nx.DiGraph:
        G = self._model.graph
        source = G.graph["source_bus"]
        reachable = {source} | set(nx.descendants(G, source))

        segments = self._model.segments_df
        enabled = segments[segments["enabled"]].copy()
        enabled["bus1"] = enabled["bus1"].str.lower()
        enabled["bus2"] = enabled["bus2"].str.lower()
        enabled = enabled[enabled["bus1"] != enabled["bus2"]]

        full_graph = nx.DiGraph()
        for _, row in enabled.iterrows():
            full_graph.add_edge(
                row["bus1"], row["bus2"],
                name=row["name"],
                type=row["type"],
            )

        loads_df = self._model.loads_df
        if loads_df is not None and not loads_df.empty:
            for _, row in loads_df.iterrows():
                bus = str(row["bus1"]).split(".")[0].lower()
                if bus not in full_graph:
                    full_graph.add_node(
                        bus,
                        type="load_bus",
                        element_name=f"load.{row['name']}",
                    )

        isolated_buses = set(full_graph.nodes()) - reachable
        return full_graph.subgraph(isolated_buses).copy()

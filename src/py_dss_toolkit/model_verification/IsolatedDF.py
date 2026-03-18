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
    def _isolated_records(self) -> list:
        return self._create_isolated_records()

    @property
    def isolated_df(self) -> pd.DataFrame:
        """DataFrame of enabled segments and shunt elements not reachable from the source bus."""
        return pd.DataFrame(self._isolated_records, columns=["element_name", "bus1", "bus2", "type"])

    def _create_isolated_records(self) -> list:
        G = self.isolated_graph
        data = []

        for u, v, attrs in G.edges(data=True):
            data.append({
                "element_name": attrs.get("name", ""),
                "bus1": u,
                "bus2": v,
                "type": "segment",
            })

        for node, attrs in G.nodes(data=True):
            shunt_elements = attrs.get("shunt_elements", [])
            for elem_name, _elem_type in shunt_elements:
                data.append({
                    "element_name": elem_name,
                    "bus1": node,
                    "bus2": "",
                    "type": "shunt",
                })

        return data

    @property
    def isolated_graph(self) -> nx.DiGraph:
        """DiGraph of all buses and enabled segments not reachable from the source bus.

        Nodes that come exclusively from shunt elements (PC elements and shunt
        PD elements like capacitors) with no segment endpoint carry
        ``shunt_elements`` as a list of (element_name, element_type).
        Edge attributes mirror the segment data: ``name``, ``type``.
        """
        return self._build_isolated_graph()

    @property
    def isolated_subgraphs(self) -> List[nx.DiGraph]:
        """One DiGraph per weakly-connected isolated island.

        Useful for analyzing or visualizing each disconnected component
        independently (e.g. to count elements per island or layout each one).
        """
        G = self.isolated_graph
        return [
            nx.DiGraph(G.subgraph(component))
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

        shunt_by_bus: dict = {}

        pc_df = self._model.enabled_pc_elements_df
        if pc_df is not None:
            for _, row in pc_df.iterrows():
                shunt_by_bus.setdefault(row["bus1"], []).append(
                    (row["name"], row["type"]))

        pd_df = self._model.enabled_pd_elements_df
        if pd_df is not None:
            shunt_pd = pd_df[(pd_df["bus2"] == "") | (pd_df["bus1"] == pd_df["bus2"])]
            for _, row in shunt_pd.iterrows():
                shunt_by_bus.setdefault(row["bus1"], []).append(
                    (row["name"], row["type"]))

        for bus, elements in shunt_by_bus.items():
            if bus not in full_graph:
                full_graph.add_node(bus, shunt_elements=elements)
            else:
                full_graph.nodes[bus]["shunt_elements"] = elements

        isolated_buses = set(full_graph.nodes()) - reachable
        return nx.DiGraph(full_graph.subgraph(isolated_buses))

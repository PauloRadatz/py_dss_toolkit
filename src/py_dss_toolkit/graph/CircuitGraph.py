# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import networkx as nx
import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.graph.GraphBuilder import GraphBuilder
from py_dss_toolkit.model.ModelQueries import ModelQueries


class CircuitGraph(ModelQueries):
    """Main facade for graph-based circuit topology queries.

    The graph is built lazily on first access and cached.  Call
    :meth:`refresh` after modifying the circuit to force a rebuild.
    """

    def __init__(self, dss: DSS):
        self._dss = dss
        self._cached_graph = None
        ModelQueries.__init__(self, dss)

    @property
    def graph(self) -> nx.MultiDiGraph:
        """Directed multigraph: nodes = buses, edges = PD elements."""
        if self._cached_graph is None:
            self._cached_graph = GraphBuilder.build(self._dss)
        return self._cached_graph

    @property
    def graph_df(self) -> pd.DataFrame:
        """Edge list as a DataFrame (bus1, bus2, and all edge attributes).

        Includes all parallel edges between the same bus pair.
        """
        G = self.graph
        records = []
        for u, v, data in G.edges(data=True):
            record = {"bus1": u, "bus2": v}
            record.update(data)
            records.append(record)
        return pd.DataFrame(records)

    def refresh(self) -> None:
        """Invalidate cached graph so the next access rebuilds it."""
        self._cached_graph = None

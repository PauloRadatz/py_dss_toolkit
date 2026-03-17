# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import networkx as nx
import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.BusesDataDF import BusesDataDF
from py_dss_toolkit.model.ElementData import ElementData
from py_dss_toolkit.model.ElementDataDFs import ElementDataDFs
from py_dss_toolkit.model.ModelQueries import ModelQueries
from py_dss_toolkit.model.ModelUtils import ModelUtils
from py_dss_toolkit.model.PCElementsDF import PCElementsDF
from py_dss_toolkit.model.PCElementsQueries import PCElementsQueries
from py_dss_toolkit.model.SegmentsDF import SegmentsDF
from py_dss_toolkit.model.SummaryModelData import SummaryModelData


class ModelBase(
    ElementDataDFs,
    BusesDataDF,
    SummaryModelData,
    ElementData,
    SegmentsDF,
    PCElementsDF,
    ModelUtils,
    ModelQueries,
    PCElementsQueries,
):

    def __init__(self, dss: DSS):
        self._dss = dss
        from py_dss_toolkit.graph.CircuitGraph import CircuitGraph
        self._circuit_graph = CircuitGraph(self._dss, self)
        ElementDataDFs.__init__(self, self._dss)
        BusesDataDF.__init__(self, self._dss)
        SummaryModelData.__init__(self, self._dss)
        ElementData.__init__(self, self._dss)
        SegmentsDF.__init__(self, self._dss)
        PCElementsDF.__init__(self, self._dss)
        ModelUtils.__init__(self, self._dss)
        ModelQueries.__init__(self, self._dss)
        PCElementsQueries.__init__(self, self._dss)

    @property
    def graph(self) -> nx.MultiDiGraph:
        """Directed multigraph: nodes = buses, edges = PD elements (including parallel)."""
        return self._circuit_graph.graph

    @property
    def graph_df(self) -> pd.DataFrame:
        """Edge list as a DataFrame (bus1, bus2, and all edge attributes).

        Includes all parallel edges between the same bus pair.
        """
        return self._circuit_graph.graph_df

    def refresh_graph(self) -> None:
        """Invalidate cached graph so the next access rebuilds it."""
        self._circuit_graph.refresh()

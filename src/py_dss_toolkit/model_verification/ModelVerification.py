# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS

from py_dss_toolkit.model.ModelBase import ModelBase
from py_dss_toolkit.model_verification.IsolatedDF import IsolatedDF
from py_dss_toolkit.model_verification.LoadsTransformerVoltageDF import LoadsTransformerVoltageDF
from py_dss_toolkit.model_verification.LoopEdgesDF import LoopEdgesDF
from py_dss_toolkit.model_verification.NodesConnectionsParentChildDF import NodesConnectionsParentChildDF
from py_dss_toolkit.model_verification.NodesConnectionsPropagatedDF import NodesConnectionsPropagatedDF
from py_dss_toolkit.model_verification.ReversedSegmentsDF import ReversedSegmentsDF
from py_dss_toolkit.model_verification.SameBusesSegmentsDF import SameBusesSegmentsDF


class ModelVerification(
    IsolatedDF,
    SameBusesSegmentsDF,
    ReversedSegmentsDF,
    NodesConnectionsParentChildDF,
    NodesConnectionsPropagatedDF,
    LoadsTransformerVoltageDF,
    LoopEdgesDF,
):
    """Facade for model verification checks.

    Exposes: isolated_df, isolated_graph, isolated_subgraphs, same_buses_segments_df,
    reversed_segments_df, nodes_connections_parent_child_df, nodes_connections_propagated_df,
    loads_transformer_voltage_df, loop_edges_df, and is_radial (True if circuit has no loops).
    """

    def __init__(self, dss: DSS, model: ModelBase):
        self._dss = dss
        self._model = model
        IsolatedDF.__init__(self, self._dss, self._model)
        SameBusesSegmentsDF.__init__(self, self._model)
        ReversedSegmentsDF.__init__(self, self._model)
        NodesConnectionsParentChildDF.__init__(self, self._dss, self._model)
        NodesConnectionsPropagatedDF.__init__(self, self._dss, self._model)
        LoadsTransformerVoltageDF.__init__(self, self._dss, self._model)
        LoopEdgesDF.__init__(self, self._model)

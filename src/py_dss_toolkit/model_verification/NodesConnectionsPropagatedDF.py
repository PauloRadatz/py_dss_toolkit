# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from collections import deque

import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.ModelBase import ModelBase
from py_dss_toolkit.model_verification.NodesConnectionsParentChildDF import (
    _normalize_nodes,
    _phase_nodes,
    _has_phase_issue,
    _collect_pc_elements,
)


def _get_source_phases(dss: DSS) -> set:
    """Phase nodes (1,2,3) available at the Vsource bus.

    Parses the Vsource bus connection (e.g. A.1.2.3 -> {1,2,3}).
    If no nodes specified, uses vsources.phases to infer.
    """
    dss.vsources.first()
    if dss.vsources.count == 0:
        return {"1", "2", "3"}
    dss.circuit.set_active_element(f"Vsource.{dss.vsources.name}")
    bus_full = dss.cktelement.bus_names[0]
    parts = bus_full.split(".")
    nodes = parts[1:] if len(parts) > 1 else []
    if not nodes:
        nph = int(getattr(dss.vsources, "phases", 3) or 3)
        nodes = [str(i) for i in range(1, nph + 1)]
    return _phase_nodes(nodes)


class NodesConnectionsPropagatedDF:
    """Propagated node-connection check via BFS from the source bus.

    Unlike the parent-child check (which compares each element only against its
    immediate parent), this walk tracks *validated phases* at every bus.  When
    an element is flagged, downstream elements are **not** cascaded -- they are
    compared against the parent's validated phases instead.

    Parallel segments between the same bus pair are aggregated: the union of
    nodes1 is checked against the parent's validated phases, and the union of
    nodes2 becomes the validated phases at the destination bus.
    """

    def __init__(self, dss: DSS, model: ModelBase):
        self._dss = dss
        self._model = model

    @property
    def nodes_connections_propagated_df(self) -> pd.DataFrame:
        """DataFrame of propagated phase-connection issues."""
        return self._check_propagated()

    def _check_propagated(self) -> pd.DataFrame:
        G = self._model.graph
        source = G.graph.get("source_bus", "")
        if not source:
            return self._empty_df()

        source_phases = _get_source_phases(self._dss)
        validated: dict[str, set] = {source: source_phases}
        rows: list[list] = []

        queue: deque[str] = deque([source])
        visited: set[str] = {source}

        while queue:
            u = queue.popleft()
            parent_validated = validated[u]

            for v in G.successors(u):
                if v in visited:
                    continue
                visited.add(v)

                all_edges = list(G[u][v].values())
                all_nodes1_phases: set = set()
                all_nodes2_phases: set = set()
                edge_names: list = []
                for edata in all_edges:
                    all_nodes1_phases |= _phase_nodes(edata.get("nodes1", []))
                    all_nodes2_phases |= _phase_nodes(edata.get("nodes2", []))
                    edge_names.append(edata.get("name", ""))

                if not all_nodes1_phases or not all_nodes1_phases.issubset(parent_validated):
                    combined_nodes1 = sorted(all_nodes1_phases) if all_nodes1_phases else ["1", "2", "3"]
                    rows.append([
                        "",
                        u,
                        sorted(parent_validated),
                        ", ".join(edge_names),
                        u,
                        combined_nodes1,
                    ])
                    validated[v] = parent_validated
                else:
                    validated[v] = all_nodes2_phases

                queue.append(v)

        pc_at_bus = _collect_pc_elements(self._dss)
        for bus, valid_phases in validated.items():
            for elem_name, elem_nodes in pc_at_bus.get(bus, []):
                if _has_phase_issue(list(valid_phases), elem_nodes):
                    rows.append([
                        "",
                        bus,
                        sorted(valid_phases),
                        elem_name,
                        bus,
                        elem_nodes,
                    ])

        return pd.DataFrame(
            rows,
            columns=["parent_name", "parent_bus", "parent_node",
                      "element_name", "element_bus", "element_node"],
        )

    @staticmethod
    def _empty_df() -> pd.DataFrame:
        return pd.DataFrame(
            columns=["parent_name", "parent_bus", "parent_node",
                      "element_name", "element_bus", "element_node"],
        )

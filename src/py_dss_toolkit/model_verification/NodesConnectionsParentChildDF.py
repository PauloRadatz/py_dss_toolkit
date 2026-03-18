# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.ModelBase import ModelBase

_NEUTRAL_NODES = {"0", "4"}
_PHASE_NODES = {"1", "2", "3"}


def _normalize_nodes(nodes) -> list:
    """Return node list; empty means default 1,2,3."""
    if not nodes:
        return ["1", "2", "3"]
    return [str(n) for n in nodes]


def _phase_nodes(nodes) -> set:
    """Phase nodes only (1,2,3), excluding neutral."""
    normalized = _normalize_nodes(nodes)
    return {n for n in normalized if n in _PHASE_NODES}


def _has_phase_issue(parent_nodes, child_nodes) -> bool:
    """True if child has a phase (1,2,3) the parent does not provide.

    Neutral (0,4) on the child is allowed even if parent lacks it.
    Child with only neutral is invalid.
    """
    parent_phases = _phase_nodes(parent_nodes)
    child_phases = _phase_nodes(child_nodes)
    if not child_phases:
        return True
    return not child_phases.issubset(parent_phases)


def _shunt_elements_by_bus(model) -> dict:
    """Bus -> list of (element_name, nodes) for shunt elements needing phase validation.

    Includes PC elements (loads, generators, pvsystems, storage) and
    shunt PD elements (wye capacitors: bus1 == bus2; delta capacitors: bus2 empty).
    """
    result: dict = {}
    pc_df = model.enabled_pc_elements_df
    if pc_df is not None:
        for _, row in pc_df.iterrows():
            result.setdefault(row["bus1"], []).append((row["name"], row["nodes1"]))

    pd_df = model.enabled_pd_elements_df
    if pd_df is not None:
        shunt = pd_df[(pd_df["bus2"] == "") | (pd_df["bus1"] == pd_df["bus2"])]
        for _, row in shunt.iterrows():
            result.setdefault(row["bus1"], []).append((row["name"], row["nodes1"]))

    return result


class NodesConnectionsParentChildDF:
    """Check whether phase connections are correct between elements at each bus.

    Includes PD elements (lines, transformers, reactors) and PC elements
    (loads, generators, capacitors). Nodes 0 and 4 (neutral) are handled
    specially -- transformer secondary can have them while primary does not.

    Parallel segments between the same bus pair are aggregated: the
    "parent phases" at a bus is the union of nodes2 from all incoming
    segments.
    """

    def __init__(self, dss: DSS, model: ModelBase):
        self._dss = dss
        self._model = model

    @property
    def _nodes_connections_parent_child_records(self) -> list:
        return self._create_nodes_connections_parent_child_records()

    @property
    def nodes_connections_parent_child_df(self) -> pd.DataFrame:
        """DataFrame of phase-connection issues between parent and child elements."""
        return pd.DataFrame(
            self._nodes_connections_parent_child_records,
            columns=["parent_name", "parent_bus", "parent_node", "element_name", "element_bus", "element_node"],
        )

    def _create_nodes_connections_parent_child_records(self) -> list:
        """Check phase connections for PD and PC elements at each bus."""
        bus_parent_phases: dict[str, set] = {}
        bus_parent_names: dict[str, list] = {}
        bus_children: dict[str, list[tuple[str, list]]] = {}

        for u, v, data in self._model.graph.edges(data=True):
            nodes1 = _normalize_nodes(data.get("nodes1", []))
            nodes2 = _normalize_nodes(data.get("nodes2", []))
            name = data.get("name", "")

            bus_parent_phases.setdefault(v, set()).update(_phase_nodes(nodes2))
            bus_parent_names.setdefault(v, []).append(name)
            bus_children.setdefault(u, []).append((name, nodes1))

        rows = []

        for bus in bus_parent_phases:
            parent_phases = bus_parent_phases[bus]
            parent_names = bus_parent_names[bus]
            parent_label = ", ".join(parent_names)
            parent_nodes_list = sorted(parent_phases)
            for child_name, child_nodes in bus_children.get(bus, []):
                if _has_phase_issue(parent_nodes_list, child_nodes):
                    rows.append([
                        parent_label,
                        bus,
                        parent_nodes_list,
                        child_name,
                        bus,
                        child_nodes,
                    ])

        for bus, children in bus_children.items():
            if bus in bus_parent_phases or len(children) < 2:
                continue
            all_phases: set = set()
            all_names: list = []
            for name, nodes in children:
                all_phases.update(_phase_nodes(nodes))
                all_names.append(name)
            ref_label = ", ".join(all_names)
            ref_nodes = sorted(all_phases)
            for child_name, child_nodes in children:
                if _has_phase_issue(ref_nodes, child_nodes):
                    rows.append([
                        ref_label,
                        bus,
                        ref_nodes,
                        child_name,
                        bus,
                        child_nodes,
                    ])

        pc_at_bus = _shunt_elements_by_bus(self._model)

        for bus in bus_parent_phases:
            parent_phases = bus_parent_phases[bus]
            parent_names = bus_parent_names[bus]
            parent_label = ", ".join(parent_names)
            parent_nodes_list = sorted(parent_phases)
            for elem_name, elem_nodes in pc_at_bus.get(bus, []):
                if _has_phase_issue(parent_nodes_list, elem_nodes):
                    rows.append([
                        parent_label,
                        bus,
                        parent_nodes_list,
                        elem_name,
                        bus,
                        elem_nodes,
                    ])

        all_buses = set(self._model.graph.nodes())
        for bus in all_buses:
            if bus in bus_parent_phases:
                continue
            out_segments = bus_children.get(bus, [])
            if not out_segments:
                continue
            all_phases_set: set = set()
            all_names_list: list = []
            for name, nodes in out_segments:
                all_phases_set.update(_phase_nodes(nodes))
                all_names_list.append(name)
            ref_label = ", ".join(all_names_list)
            ref_nodes = sorted(all_phases_set)
            for elem_name, elem_nodes in pc_at_bus.get(bus, []):
                if _has_phase_issue(ref_nodes, elem_nodes):
                    rows.append([
                        ref_label,
                        bus,
                        ref_nodes,
                        elem_name,
                        bus,
                        elem_nodes,
                    ])

        return rows

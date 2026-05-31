# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import math
from collections import defaultdict, deque
from typing import Any, Dict, List, Set, Tuple

import networkx as nx
from py_dss_interface import DSS

from typing import Optional

from py_dss_toolkit.model.BusesDataDF import BusesDataDF
from py_dss_toolkit.model.ElementDataDFs import ElementDataDFs
from py_dss_toolkit.model.SegmentsDF import SegmentsDF


class GraphBuilder:
    """Builds a directed multigraph (nx.MultiDiGraph) from an OpenDSS circuit.

    Nodes represent buses and edges represent PD elements (lines, transformers,
    reactors).  Parallel elements between the same bus pair are stored as
    separate edges keyed by segment name.  Edge direction is oriented away from
    the source bus via BFS so that upstream/downstream traversals are
    straightforward.
    """

    @staticmethod
    def build(dss: DSS, model: Optional[object] = None) -> nx.MultiDiGraph:
        source_bus = GraphBuilder._find_source_bus(dss)
        bus_data = GraphBuilder._collect_bus_data(dss)
        edge_list, adjacency = GraphBuilder._collect_edges(dss, model)

        G = nx.MultiDiGraph()
        G.graph["source_bus"] = source_bus

        for bus_name, attrs in bus_data.items():
            G.add_node(bus_name, **attrs)

        source_vll, source_vln = GraphBuilder._source_voltage(dss)
        G.nodes[source_bus]["connection_type"] = "ln"
        G.nodes[source_bus]["vll"] = source_vll
        G.nodes[source_bus]["vln"] = source_vln
        G.nodes[source_bus]["feeding_transformer"] = ""

        visited: Set[str] = {source_bus}
        queue: deque = deque([source_bus])
        while queue:
            current = queue.popleft()
            cur = G.nodes[current]
            current_conn = cur.get("connection_type", "ln")
            current_vll = cur.get("vll", 0.0)
            current_vln = cur.get("vln", 0.0)
            for neighbor in adjacency.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    pair_key = frozenset((current, neighbor))
                    neighbor_conn = current_conn
                    neighbor_vll = current_vll
                    neighbor_vln = current_vln
                    neighbor_feeding = cur.get("feeding_transformer", "")
                    xfmr_resolved = False
                    for attrs in edge_list.get(pair_key, []):
                        attrs = dict(attrs)
                        if current != attrs["bus1_dss"]:
                            GraphBuilder._swap_edge_direction(attrs)
                            attrs["reversed"] = True
                        else:
                            attrs["reversed"] = False
                        G.add_edge(current, neighbor, key=attrs["name"], **attrs)
                        if not xfmr_resolved and attrs.get("type") == "transformer":
                            neighbor_conn = GraphBuilder._connection_type_from_transformer(attrs)
                            neighbor_vll, neighbor_vln = GraphBuilder._feeding_voltage_from_transformer(attrs)
                            neighbor_feeding = GraphBuilder._transformer_obj_name_from_segment(attrs["name"])
                            xfmr_resolved = True
                    G.nodes[neighbor]["connection_type"] = neighbor_conn
                    G.nodes[neighbor]["vll"] = neighbor_vll
                    G.nodes[neighbor]["vln"] = neighbor_vln
                    G.nodes[neighbor]["feeding_transformer"] = neighbor_feeding

        return G

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _find_source_bus(dss: DSS) -> str:
        dss.vsources.first()
        dss.circuit.set_active_element(f"Vsource.{dss.vsources.name}")
        return dss.cktelement.bus_names[0].split(".")[0].lower()

    @staticmethod
    def _collect_bus_data(dss: DSS) -> Dict[str, Dict[str, Any]]:
        buses_df = BusesDataDF(dss).buses_df
        result: Dict[str, Dict[str, Any]] = {}
        for _, row in buses_df.iterrows():
            bus_name = row["name"].lower()
            result[bus_name] = row.drop("name").to_dict()
        return result

    @staticmethod
    def _collect_edges(dss: DSS, model: Optional[object] = None) -> Tuple[Dict[frozenset, List[Dict[str, Any]]], Dict[str, Set[str]]]:
        if model is not None and hasattr(model, "segments_df"):
            segments_df = model.segments_df
        else:
            segments_df = SegmentsDF(dss).segments_df
        enabled_segments = segments_df[segments_df["enabled"]]

        tr_lookup = GraphBuilder._build_transformer_lookup(dss)

        edge_list: Dict[frozenset, List[Dict[str, Any]]] = defaultdict(list)
        adjacency: Dict[str, Set[str]] = defaultdict(set)

        for _, row in enabled_segments.iterrows():
            bus1 = row["bus1"].lower()
            bus2 = row["bus2"].lower()

            if bus1 == bus2:
                continue

            attrs: Dict[str, Any] = dict(
                name=row["name"],
                type=row["type"],
                bus1_dss=bus1,
                bus2_dss=bus2,
                nodes1=row["nodes1"],
                nodes2=row["nodes2"],
                phases=len(row["nodes1"]),
                enabled=True,
            )

            if row["type"] == "transformer":
                tr_name = row["name"].split(".")[1]
                if tr_name in tr_lookup:
                    GraphBuilder._enrich_transformer(attrs, tr_lookup[tr_name])

            key = frozenset((bus1, bus2))
            edge_list[key].append(attrs)
            adjacency[bus1].add(bus2)
            adjacency[bus2].add(bus1)

        return edge_list, adjacency

    @staticmethod
    def _build_transformer_lookup(dss: DSS) -> Dict[str, Dict[str, Any]]:
        transformers_df = ElementDataDFs(dss).transformers_df
        if transformers_df is None:
            return {}
        lookup: Dict[str, Dict[str, Any]] = {}
        for _, tr_row in transformers_df.iterrows():
            lookup[tr_row["name"]] = tr_row.to_dict()
        return lookup

    @staticmethod
    def _transformer_obj_name_from_segment(segment_name: str) -> str:
        """OpenDSS object name without the ``Transformer.`` class prefix (segment names are ``class.name``)."""
        parts = str(segment_name).split(".", 1)
        if len(parts) == 2 and parts[0].lower() == "transformer":
            return parts[1]
        return str(segment_name)

    @staticmethod
    def _source_voltage(dss: DSS) -> Tuple[float, float]:
        """``(vll, vln)`` in kV derived from the Vsource."""
        dss.vsources.first()
        kv_base = dss.vsources.base_kv
        if dss.vsources.phases == 1:
            return (round(kv_base * math.sqrt(3), 4), round(kv_base, 4))
        return (round(kv_base, 4), round(kv_base / math.sqrt(3), 4))

    @staticmethod
    def _feeding_voltage_from_transformer(tr: Dict[str, Any]) -> Tuple[float, float]:
        """``(vll, vln)`` in kV derived from transformer edge attributes."""
        phases = tr.get("phases", 3)
        kv_secondary = tr.get("kv_secondary", 0.0)
        num_windings = tr.get("num_windings", 2)

        if phases == 3:
            vll = kv_secondary
            vln = kv_secondary / math.sqrt(3)
        elif phases == 1:
            if num_windings >= 3:
                vln = kv_secondary
                vll = 2 * vln
            else:
                _phase_nodes = {"1", "2", "3"}
                _nodes2 = [str(n) for n in tr.get("nodes2", [])]
                _phase_count = sum(1 for n in _nodes2 if n in _phase_nodes)
                if _phase_count >= 2:
                    vll = kv_secondary
                    vln = vll / math.sqrt(3)
                else:
                    vln = kv_secondary
                    vll = vln * math.sqrt(3)
        else:
            vll = kv_secondary
            vln = kv_secondary / math.sqrt(3)

        return (round(vll, 4), round(vln, 4))

    @staticmethod
    def _connection_type_from_transformer(tr: Dict[str, Any]) -> str:
        """Derive ``'ln'`` or ``'ll'`` from transformer edge attributes."""
        phases = tr.get("phases", 3)
        num_windings = tr.get("num_windings", 2)

        if phases == 1:
            if num_windings >= 3:
                return "ln"
            _phase_nodes = {"1", "2", "3"}
            _nodes2 = [str(n) for n in tr.get("nodes2", [])]
            _phase_count = sum(1 for n in _nodes2 if n in _phase_nodes)
            return "ll" if _phase_count >= 2 else "ln"

        conn_secondary = tr.get("conn_secondary", "wye")
        return "ll" if conn_secondary == "delta" else "ln"

    @staticmethod
    def _swap_edge_direction(attrs: Dict[str, Any]) -> None:
        """Swap direction-sensitive attributes so they match the BFS edge direction.

        bus1_dss and bus2_dss are NOT swapped; they always reflect the DSS/model
        segment order. nodes1/nodes2 stay with their respective buses.
        """
        if attrs.get("type") == "transformer":
            if "kv_primary" in attrs:
                attrs["kv_primary"], attrs["kv_secondary"] = attrs["kv_secondary"], attrs["kv_primary"]
            if "conn_primary" in attrs:
                attrs["conn_primary"], attrs["conn_secondary"] = attrs["conn_secondary"], attrs["conn_primary"]
            if "kvs" in attrs:
                attrs["kvs"] = list(reversed(attrs["kvs"]))
            if "conns" in attrs:
                attrs["conns"] = list(reversed(attrs["conns"]))

    @staticmethod
    def _enrich_transformer(attrs: Dict[str, Any], tr_props: Dict[str, Any]) -> None:
        attrs["phases"] = int(tr_props.get("phases", len(attrs["nodes1"])))
        num_windings = int(tr_props.get("windings", 2))
        attrs["num_windings"] = num_windings

        conns = GraphBuilder._parse_dss_list(tr_props.get("conns", ""))
        kvs = GraphBuilder._parse_dss_list(tr_props.get("kvs", ""))

        attrs["conns"] = conns
        attrs["kvs"] = [float(v) for v in kvs]
        attrs["kv_primary"] = float(kvs[0])
        attrs["kv_secondary"] = float(kvs[1])
        attrs["conn_primary"] = conns[0].lower()
        attrs["conn_secondary"] = conns[1].lower()

        if num_windings >= 3:
            attrs["kv_tertiary"] = float(kvs[2])
            attrs["conn_tertiary"] = conns[2].lower()
        else:
            attrs["kv_tertiary"] = float("nan")
            attrs["conn_tertiary"] = None

    @staticmethod
    def _parse_dss_list(value: str) -> list:
        """Parse a DSS bracketed list like ``[wye, wye]`` or ``[12.47 4.16]``."""
        cleaned = str(value).replace("[", "").replace("]", "").strip()
        if not cleaned:
            return []
        if "," in cleaned:
            return [v.strip() for v in cleaned.split(",") if v.strip()]
        return [v.strip() for v in cleaned.split() if v.strip()]

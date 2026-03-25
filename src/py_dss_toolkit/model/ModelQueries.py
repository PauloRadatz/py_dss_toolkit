# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import collections
from typing import Any, Dict, List, Optional, Tuple

import networkx as nx
import pandas as pd
from py_dss_interface import DSS


class ModelQueries:
    """Mixin that provides topology query methods over a circuit graph.

    Requires ``self.graph`` (a ``nx.MultiDiGraph``) to be supplied by the
    composing class (i.e. :class:`ModelBase`).

    Public ``*_df`` methods return DataFrames. Private ``*_records`` methods
    return lists of dicts (JSON-serializable) for use in APIs (e.g. FastAPI).
    """

    def __init__(self, dss: DSS):
        self._dss = dss

    def _validate_bus(self, bus: str) -> str:
        if not self.is_bus_in_model(bus):
            raise ValueError(f"Bus '{bus}' does not exist in the circuit.")
        return bus

    def _validate_segment(self, segment: str) -> str:
        segment = segment.lower()
        if not self.is_element_in_model(segment.split(".")[0], segment.split(".")[1]):
            raise ValueError(f"Segment '{segment}' does not exist in the circuit.")
        return segment

    def _empty_bus_df(self) -> pd.DataFrame:
        buses = self.buses_df
        prop_cols = [c for c in buses.columns if c != "name"]
        return pd.DataFrame(columns=["bus", "level"] + prop_cols)

    def _empty_segment_df(self) -> pd.DataFrame:
        edge_cols = [c for c in self.graph_df.columns if c != "name"]
        return pd.DataFrame(columns=["segment", "level"] + list(edge_cols))

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    @property
    def source_bus(self) -> str:
        """Circuit element's bus name used as the root of the directed graph (typically the ``sourcebus`` bus).

        Returns:
            str: Lowercase bus name from ``graph.graph['source_bus']``; upstream/downstream
            queries are relative to this node.
        """
        return self.graph.graph["source_bus"]

    def _upstream_path(self, bus: str) -> List[str]:
        bus = bus.lower()
        G = self.graph
        source = G.graph["source_bus"]
        try:
            return list(nx.shortest_path(G, source, bus))
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def upstream_transformer(self, bus: str) -> Optional[Dict[str, Any]]:
        """Edge attributes of the nearest upstream transformer feeding *bus*.

        Returns ``None`` when no transformer exists on the path to the source.
        When multiple parallel transformers exist between the same bus pair,
        returns the first one found.
        """
        path = self._upstream_path(bus)
        if len(path) < 2:
            return None
        G = self.graph
        for i in range(len(path) - 1, 0, -1):
            for _key, edge_data in G[path[i - 1]][path[i]].items():
                if edge_data.get("type") == "transformer":
                    return dict(edge_data)
        return None

    # ------------------------------------------------------------------
    # Topology queries: upstream/downstream segments and buses
    # ------------------------------------------------------------------

    def _segment_to_buses(self, segment: str) -> Optional[Tuple[str, str]]:
        """Look up segment by name; return (bus1, bus2) or None if not found."""
        segment = segment.lower()
        df = self.graph_df
        match = df[df["name"] == segment]
        if match.empty:
            return None
        row = match.iloc[0]
        return str(row["bus1"]).lower(), str(row["bus2"]).lower()

    def _upstream_bus_of_pair(self, bus1: str, bus2: str) -> str:
        """Return the bus closer to source (shorter upstream path)."""
        path1 = self._upstream_path(bus1)
        path2 = self._upstream_path(bus2)
        return bus1 if len(path1) <= len(path2) else bus2

    def _segments_between_pair(self, b1: str, b2: str) -> List[Dict[str, Any]]:
        """All segments between bus pair (order-independent)."""
        df = self.graph_df
        mask = ((df["bus1"] == b1) & (df["bus2"] == b2)) | (
            (df["bus1"] == b2) & (df["bus2"] == b1)
        )
        return df[mask].to_dict("records")

    def segments_at_bus_df(self, bus: str) -> pd.DataFrame:
        """DataFrame of all segments connected to *bus* (incoming and outgoing).

        Returns graph_df rows where bus is either bus1 or bus2, with an added
        ``direction`` column: ``'outgoing'`` if bus is bus1, ``'incoming'`` if bus is bus2.
        """
        self._validate_bus(bus)
        df = self.graph_df
        mask = (df["bus1"] == bus) | (df["bus2"] == bus)
        result = df[mask].copy()
        if result.empty:
            return self._empty_segment_df()
        result["direction"] = result.apply(
            lambda r: "outgoing" if str(r["bus1"]).lower() == bus else "incoming",
            axis=1,
        )
        return result.reset_index(drop=True)

    def upstream_transformers_df(self, bus: str) -> pd.DataFrame:
        """DataFrame of all transformers on the path from source to *bus*.

        Columns include segment name, level (1 = closest to source), and
        transformer attributes (kv_primary, kv_secondary, conn_primary, etc.).
        """
        self._validate_bus(bus)
        path = self._upstream_path(bus)
        if len(path) < 2:
            return self._empty_segment_df()
        G = self.graph
        records: List[Dict[str, Any]] = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            for _key, edge_data in G[u][v].items():
                if edge_data.get("type") == "transformer":
                    rec = dict(edge_data)
                    rec["level"] = i + 1
                    rec["segment"] = rec.get("name", "")
                    records.append(rec)
        if not records:
            return self._empty_segment_df()
        return pd.DataFrame(records)

    # -- Upstream segments from bus ---

    def _upstream_segments_from_bus_records(self, bus: str) -> List[Dict[str, Any]]:
        """Records of segments on path from source to *bus* with level (1 = closest to source)."""
        bus = bus.lower()
        path = self._upstream_path(bus)
        if len(path) < 2:
            return []
        result: List[Dict[str, Any]] = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            for seg in self._segments_between_pair(u, v):
                rec = dict(seg)
                rec["level"] = i + 1
                result.append(rec)
        return result

    def upstream_segments_from_bus_df(self, bus: str) -> pd.DataFrame:
        """DataFrame of segments upstream of *bus* with columns including ``segment`` (name) and ``level``."""
        self._validate_bus(bus)
        records = self._upstream_segments_from_bus_records(bus)
        if not records:
            return self._empty_segment_df()
        df = pd.DataFrame(records)
        return df.rename(columns={"name": "segment"})

    # -- Downstream segments from bus ---

    def _downstream_segments_from_bus_records(self, bus: str) -> List[Dict[str, Any]]:
        """Records of segments downstream of *bus* with level (1 = immediate downstream)."""
        bus = bus.lower()
        G = self.graph
        if bus not in G:
            return []
        result: List[Dict[str, Any]] = []
        visited: set[str] = set()
        queue: collections.deque[Tuple[str, int]] = collections.deque([(bus, 0)])
        while queue:
            u, level = queue.popleft()
            for v in G.successors(u):
                for seg in self._segments_between_pair(u, v):
                    rec = dict(seg)
                    rec["level"] = level + 1
                    result.append(rec)
                if v not in visited:
                    visited.add(v)
                    queue.append((v, level + 1))
        return sorted(result, key=lambda r: (r["level"], r.get("name", "")))

    def downstream_segments_from_bus_df(self, bus: str) -> pd.DataFrame:
        """DataFrame of segments downstream of *bus* with columns including ``segment`` (name) and ``level``."""
        self._validate_bus(bus)
        records = self._downstream_segments_from_bus_records(bus)
        if not records:
            return self._empty_segment_df()
        df = pd.DataFrame(records)
        return df.rename(columns={"name": "segment"})

    # -- Upstream/downstream segments from segment ---

    def upstream_segments_from_segment_df(self, segment: str) -> pd.DataFrame:
        """DataFrame of segments upstream of the given segment. Excludes the segment itself."""
        self._validate_segment(segment)
        pair = self._segment_to_buses(segment)
        if pair is None:
            return self._empty_segment_df()
        bus1, bus2 = pair
        upstream_bus = self._upstream_bus_of_pair(bus1, bus2)
        df = self._upstream_segments_from_bus_as_df(upstream_bus)
        seg_lower = segment.lower()
        return df[df["segment"].str.lower() != seg_lower].reset_index(drop=True)

    def downstream_segments_from_segment_df(self, segment: str) -> pd.DataFrame:
        """DataFrame of segments downstream of the given segment. Excludes the segment itself."""
        self._validate_segment(segment)
        pair = self._segment_to_buses(segment)
        if pair is None:
            return self._empty_segment_df()
        bus1, bus2 = pair
        upstream_bus = self._upstream_bus_of_pair(bus1, bus2)
        downstream_bus = bus2 if upstream_bus == bus1 else bus1
        df = self._downstream_segments_from_bus_as_df(downstream_bus)
        seg_lower = segment.lower()
        return df[df["segment"].str.lower() != seg_lower].reset_index(drop=True)

    def _upstream_segments_from_bus_as_df(self, bus: str) -> pd.DataFrame:
        """Internal: build segment DF without bus validation (bus already validated)."""
        records = self._upstream_segments_from_bus_records(bus)
        if not records:
            return self._empty_segment_df()
        df = pd.DataFrame(records)
        return df.rename(columns={"name": "segment"})

    def _downstream_segments_from_bus_as_df(self, bus: str) -> pd.DataFrame:
        """Internal: build segment DF without bus validation (bus already validated)."""
        records = self._downstream_segments_from_bus_records(bus)
        if not records:
            return self._empty_segment_df()
        df = pd.DataFrame(records)
        return df.rename(columns={"name": "segment"})

    # -- Upstream buses from bus ---

    def _upstream_buses_from_bus_records(self, bus: str) -> List[Dict[str, Any]]:
        """Records of buses upstream of *bus* (excluding bus) with level (1 = source)."""
        path = self._upstream_path(bus)
        if len(path) < 2:
            return []
        return [{"name": b, "level": i} for i, b in enumerate(path[:-1], start=1)]

    def _enrich_buses_df_with_bus_properties(self, df: pd.DataFrame) -> pd.DataFrame:
        """Join bus+level DataFrame with buses_df properties. Returns enriched DataFrame.

        Column order: bus (1st), level (2nd), then bus properties.
        """
        buses = self.buses_df.copy()
        buses["name"] = buses["name"].str.lower()
        if df.empty:
            prop_cols = [c for c in buses.columns if c != "name"]
            return pd.DataFrame(columns=["name", "level"] + prop_cols)
        result = df.merge(buses, on="name", how="left")
        other_cols = [c for c in result.columns if c not in ("name", "level")]
        return result[["name", "level"] + other_cols]

    def upstream_buses_from_bus_df(self, bus: str) -> pd.DataFrame:
        """DataFrame of buses upstream of *bus* with ``bus``, ``level``, and buses_df properties.

        Level 1 = source bus, level 2 = next upstream, etc. Excludes *bus* itself.
        """
        self._validate_bus(bus)
        records = self._upstream_buses_from_bus_records(bus)
        df = pd.DataFrame(records)
        return self._enrich_buses_df_with_bus_properties(df)

    # -- Downstream buses from bus ---

    def _downstream_buses_from_bus_records(self, bus: str) -> List[Dict[str, Any]]:
        """Records of buses downstream of *bus* with their level (1 = immediate downstream)."""
        bus = bus.lower()
        G = self.graph
        if bus not in G:
            return []
        result: List[Dict[str, Any]] = []
        visited = {bus}
        queue: collections.deque[Tuple[str, int]] = collections.deque([(bus, 0)])
        while queue:
            u, level = queue.popleft()
            for v in G.successors(u):
                if v not in visited:
                    visited.add(v)
                    result.append({"name": v, "level": level + 1})
                    queue.append((v, level + 1))
        return sorted(result, key=lambda r: (r["level"], r["name"]))

    def downstream_buses_from_bus_df(self, bus: str) -> pd.DataFrame:
        """DataFrame of buses downstream of *bus* with ``bus``, ``level``, and buses_df properties.

        Level 1 = immediate downstream neighbors. Sorted by level then bus name.
        """
        self._validate_bus(bus)
        records = self._downstream_buses_from_bus_records(bus)
        df = pd.DataFrame(records)
        return self._enrich_buses_df_with_bus_properties(df)

    # -- Upstream / downstream buses from segment ---

    def _upstream_buses_to_bus_records(self, bus: str) -> List[Dict[str, Any]]:
        """Records of buses from source to *bus* (inclusive) with level (1 = source)."""
        path = self._upstream_path(bus)
        if not path:
            return []
        return [{"name": b, "level": i} for i, b in enumerate(path, start=1)]

    def upstream_buses_from_segment_df(self, segment: str) -> pd.DataFrame:
        """DataFrame of buses upstream of the segment with ``bus``, ``level``, and buses_df properties."""
        self._validate_segment(segment)
        pair = self._segment_to_buses(segment)
        if pair is None:
            return self._empty_bus_df()
        upstream_bus = self._upstream_bus_of_pair(pair[0], pair[1])
        records = self._upstream_buses_to_bus_records(upstream_bus)
        df = pd.DataFrame(records)
        return self._enrich_buses_df_with_bus_properties(df)

    def _downstream_buses_from_segment_records(self, segment: str) -> List[Dict[str, Any]]:
        """Records of buses downstream of segment (downstream end at level 1, then 2, 3...)."""
        pair = self._segment_to_buses(segment)
        if pair is None:
            return []
        upstream_bus = self._upstream_bus_of_pair(pair[0], pair[1])
        downstream_bus = pair[1] if upstream_bus == pair[0] else pair[0]
        records = [{"name": downstream_bus, "level": 1}]
        for r in self._downstream_buses_from_bus_records(downstream_bus):
            records.append({"name": r["name"], "level": r["level"] + 1})
        return records

    def downstream_buses_from_segment_df(self, segment: str) -> pd.DataFrame:
        """DataFrame of buses downstream of the segment with ``bus``, ``level``, and buses_df properties."""
        self._validate_segment(segment)
        records = self._downstream_buses_from_segment_records(segment)
        df = pd.DataFrame(records)
        return self._enrich_buses_df_with_bus_properties(df)

    # -- Path between buses ---

    def _path_between_buses(self, bus1: str, bus2: str) -> List[str]:
        """Ordered list of buses on the path from *bus1* to *bus2* (radial tree)."""
        bus1, bus2 = bus1.lower(), bus2.lower()
        path1 = self._upstream_path(bus1)  # [source, ..., bus1]
        path2 = self._upstream_path(bus2)  # [source, ..., bus2]
        if not path1 or not path2:
            return []
        common_len = 0
        for i in range(min(len(path1), len(path2))):
            if path1[i] == path2[i]:
                common_len = i + 1
            else:
                break
        return path1[common_len - 1 :][::-1] + path2[common_len:]

    def _common_path_to_source_between_buses(self, bus1: str, bus2: str) -> List[str]:
        """Ordered list of shared upstream buses from source to the common ancestor."""
        bus1, bus2 = bus1.lower(), bus2.lower()
        path1 = self._upstream_path(bus1)
        path2 = self._upstream_path(bus2)
        if not path1 or not path2:
            return []

        common_path: List[str] = []
        for b1, b2 in zip(path1, path2):
            if b1 != b2:
                break
            common_path.append(b1)
        return common_path

    def _buses_path_between_buses_records(self, bus1: str, bus2: str) -> List[Dict[str, Any]]:
        """Records of buses on the path from *bus1* to *bus2* with level (1 = bus1, 2 = next, ...). For API use."""
        path = self._path_between_buses(bus1, bus2)
        return [{"name": b, "level": i} for i, b in enumerate(path, start=1)]

    def buses_path_between_buses_df(self, bus1: str, bus2: str) -> pd.DataFrame:
        """DataFrame of buses on the path from *bus1* to *bus2* with ``bus``, ``level``, and buses_df properties."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        records = self._buses_path_between_buses_records(bus1, bus2)
        if not records:
            return self._empty_bus_df()
        df = pd.DataFrame(records)
        return self._enrich_buses_df_with_bus_properties(df)

    def _common_path_to_source_between_buses_records(self, bus1: str, bus2: str) -> List[Dict[str, Any]]:
        """Records of the shared upstream path from source to the common ancestor."""
        path = self._common_path_to_source_between_buses(bus1, bus2)
        return [{"name": b, "level": i} for i, b in enumerate(path, start=1)]

    def common_path_to_source_between_buses_df(self, bus1: str, bus2: str) -> pd.DataFrame:
        """DataFrame of the buses shared on the path from source to both buses."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        records = self._common_path_to_source_between_buses_records(bus1, bus2)
        if not records:
            return self._empty_bus_df()
        df = pd.DataFrame(records)
        return self._enrich_buses_df_with_bus_properties(df)

    def _segments_path_between_buses_records(self, bus1: str, bus2: str) -> List[Dict[str, Any]]:
        """Records of all segments on the path from *bus1* to *bus2* (order-independent). For API use."""
        bus1, bus2 = bus1.lower(), bus2.lower()
        path = self._path_between_buses(bus1, bus2)
        if len(path) < 2:
            return []
        result: List[Dict[str, Any]] = []
        for level, (u, v) in enumerate(zip(path[:-1], path[1:]), start=1):
            for r in self._segments_between_pair(u, v):
                rec = {"segment": r.get("name", ""), "level": level, "bus1": u, "bus2": v}
                rec.update({k: val for k, val in r.items() if k not in ("name",)})
                result.append(rec)
        return result

    def segments_path_between_buses_df(self, bus1: str, bus2: str) -> pd.DataFrame:
        """DataFrame of all segments on the path from *bus1* to *bus2* (order-independent)."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        records = self._segments_path_between_buses_records(bus1, bus2)
        if not records:
            return self._empty_segment_df()
        return pd.DataFrame(records)

    # ------------------------------------------------------------------
    # Voltage queries
    # ------------------------------------------------------------------

    def feeding_voltage(self, bus: str) -> Tuple[float, float]:
        """``(vll, vln)`` in kV for *bus* based on the upstream transformer.

        Reads the ``vll`` and ``vln`` attributes directly from the graph node
        (computed during graph construction).

        Raises:
            ValueError: If *bus* does not exist in the circuit.
        """
        bus = self._validate_bus(bus)
        node = self.graph.nodes[bus]
        return (node.get("vll", 0.0), node.get("vln", 0.0))

    @property
    def bus_connection_type_map(self) -> Dict[str, str]:
        """Mapping of every bus to ``'ln'`` or ``'ll'``.

        The value is stored as a node attribute (``connection_type``) on the
        graph during construction, so this is just a view over the graph nodes.
        """
        return {
            bus: data.get("connection_type", "ln")
            for bus, data in self.graph.nodes(data=True)
        }

    def bus_connection_type(self, bus: str) -> str:
        """Whether *bus* should use ``'ln'`` or ``'ll'`` voltage.

        Reads the ``connection_type`` attribute directly from the graph node.

        Raises:
            ValueError: If *bus* does not exist in the circuit.
        """
        bus = self._validate_bus(bus)
        return self.graph.nodes[bus].get("connection_type", "ln")

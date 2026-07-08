# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

import pandas as pd
from py_dss_interface import DSS


def _safe_float(val: Any, default: float = 0.0) -> float:
    """Convert to float; return default if invalid."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return default
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _bus_from_bus1(bus1_str: Any) -> str:
    """Extract bus name from bus1 string (e.g. 'B.1.2.3' -> 'b')."""
    s = str(bus1_str).strip()
    if not s:
        return ""
    return s.split(".")[0].lower()


class PCElementsQueries:
    """Mixin for topology-aware PC element (loads, generators, PV, storage) queries.

    Requires ``self.loads_df``, ``self.generators_df``, ``self.pvsystems_df``,
    ``self.storage_df`` (from ElementDataDFs), and topology methods from ModelQueries
    (``_path_between_buses``, ``_downstream_buses_from_bus_records``, ``_validate_bus``).
    """

    def __init__(self, dss: DSS):
        self._dss = dss

    def _downstream_bus_set(self, bus: str) -> Set[str]:
        """Set of bus + all buses downstream of bus."""
        bus = bus.lower()
        result: Set[str] = {bus}
        for r in self._downstream_buses_from_bus_records(bus):
            result.add(r["name"])
        return result

    def _load_kw_kvar_at_buses(self, buses: Set[str]) -> tuple[float, float]:
        """Sum load kW and kvar at given buses (nominal values). Returns (kw, kvar)."""
        df = self.loads_df
        if df is None or df.empty:
            return (0.0, 0.0)
        cols = {c.lower() for c in df.columns}
        kw_col = "kw" if "kw" in cols else None
        kvar_col = "kvar" if "kvar" in cols else None
        bus1_col = "bus1" if "bus1" in cols else None
        if not bus1_col:
            return (0.0, 0.0)
        total_kw = 0.0
        total_kvar = 0.0
        for _, row in df.iterrows():
            elem_bus = _bus_from_bus1(row.get(bus1_col, ""))
            if elem_bus not in buses:
                continue
            if kw_col:
                total_kw += _safe_float(row.get(kw_col))
            if kvar_col:
                total_kvar += _safe_float(row.get(kvar_col))
        return (total_kw, total_kvar)

    def generator_kw_at_buses(self, buses: Set[str]) -> float:
        """Sum generator kW at given buses (nominal values)."""
        df = self.generators_df
        if df is None or df.empty:
            return 0.0
        cols = {c.lower() for c in df.columns}
        kw_col = "kw" if "kw" in cols else "kva" if "kva" in cols else None
        bus1_col = "bus1" if "bus1" in cols else None
        if not kw_col or not bus1_col:
            return 0.0
        total = 0.0
        for _, row in df.iterrows():
            elem_bus = _bus_from_bus1(row.get(bus1_col, ""))
            if elem_bus in buses:
                total += _safe_float(row.get(kw_col))
        return total

    def _pvsystem_kw_at_buses(self, buses: Set[str]) -> float:
        """Sum PV system pmpp (rated kW) at given buses (nominal values)."""
        df = self.pvsystems_df
        if df is None or df.empty:
            return 0.0
        cols = {c.lower() for c in df.columns}
        pmpp_col = "pmpp" if "pmpp" in cols else None
        bus1_col = "bus1" if "bus1" in cols else None
        if not pmpp_col or not bus1_col:
            return 0.0
        total = 0.0
        for _, row in df.iterrows():
            elem_bus = _bus_from_bus1(row.get(bus1_col, ""))
            if elem_bus in buses:
                total += _safe_float(row.get(pmpp_col))
        return total

    def _storage_kw_at_buses(self, buses: Set[str]) -> float:
        """Sum storage kwrated (discharge kW) at given buses (nominal values)."""
        df = self.storage_df
        if df is None or df.empty:
            return 0.0
        cols = {c.lower() for c in df.columns}
        kw_col = "kwrated" if "kwrated" in cols else "kw" if "kw" in cols else None
        bus1_col = "bus1" if "bus1" in cols else None
        if not kw_col or not bus1_col:
            return 0.0
        total = 0.0
        for _, row in df.iterrows():
            elem_bus = _bus_from_bus1(row.get(bus1_col, ""))
            if elem_bus in buses:
                total += _safe_float(row.get(kw_col))
        return total

    def downstream_load_kw(self, bus: str) -> float:
        """Total load kW downstream of *bus* (includes load at bus itself). Nominal values."""
        self._validate_bus(bus)
        buses = self._downstream_bus_set(bus)
        kw, _ = self._load_kw_kvar_at_buses(buses)
        return kw

    def downstream_load_kvar(self, bus: str) -> float:
        """Total load kvar downstream of *bus* (includes load at bus itself). Nominal values."""
        self._validate_bus(bus)
        buses = self._downstream_bus_set(bus)
        _, kvar = self._load_kw_kvar_at_buses(buses)
        return kvar

    def downstream_generator_kw(self, bus: str) -> float:
        """Total generator kW downstream of *bus*. Nominal values."""
        self._validate_bus(bus)
        buses = self._downstream_bus_set(bus)
        return self.generator_kw_at_buses(buses)

    def downstream_pvsystem_kw(self, bus: str) -> float:
        """Total PV system pmpp (rated kW) downstream of *bus*. Nominal values."""
        self._validate_bus(bus)
        buses = self._downstream_bus_set(bus)
        return self._pvsystem_kw_at_buses(buses)

    def downstream_storage_kw(self, bus: str) -> float:
        """Total storage kwrated downstream of *bus*. Nominal values."""
        self._validate_bus(bus)
        buses = self._downstream_bus_set(bus)
        return self._storage_kw_at_buses(buses)

    def load_between_buses_kw(self, bus1: str, bus2: str) -> float:
        """Load kW at buses on the path between *bus1* and *bus2* (inclusive). Nominal values."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        path = self._path_between_buses(bus1, bus2)
        buses = set(path) if path else set()
        kw, _ = self._load_kw_kvar_at_buses(buses)
        return kw

    def load_between_buses_kvar(self, bus1: str, bus2: str) -> float:
        """Load kvar at buses on the path between *bus1* and *bus2* (inclusive). Nominal values."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        path = self._path_between_buses(bus1, bus2)
        buses = set(path) if path else set()
        _, kvar = self._load_kw_kvar_at_buses(buses)
        return kvar

    def generator_between_buses_kw(self, bus1: str, bus2: str) -> float:
        """Generator kW at buses on the path between *bus1* and *bus2* (inclusive). Nominal values."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        path = self._path_between_buses(bus1, bus2)
        buses = set(path) if path else set()
        return self.generator_kw_at_buses(buses)

    def pvsystem_between_buses_kw(self, bus1: str, bus2: str) -> float:
        """PV system pmpp at buses on the path between *bus1* and *bus2* (inclusive). Nominal values."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        path = self._path_between_buses(bus1, bus2)
        buses = set(path) if path else set()
        return self._pvsystem_kw_at_buses(buses)

    def storage_between_buses_kw(self, bus1: str, bus2: str) -> float:
        """Storage kwrated at buses on the path between *bus1* and *bus2* (inclusive). Nominal values."""
        self._validate_bus(bus1)
        self._validate_bus(bus2)
        path = self._path_between_buses(bus1, bus2)
        buses = set(path) if path else set()
        return self._storage_kw_at_buses(buses)

    def downstream_pc_elements_df(self, bus: str) -> pd.DataFrame:
        """Per-bus breakdown of PC elements downstream: bus, element_type, name, kw, kvar, ..."""
        self._validate_bus(bus)
        buses = self._downstream_bus_set(bus)
        rows: List[Dict[str, Any]] = []

        def add_rows(df: Optional[pd.DataFrame], element_type: str, kw_col: str, kvar_col: Optional[str] = None):
            if df is None or df.empty:
                return
            cols = {c.lower() for c in df.columns}
            bus1_col = "bus1" if "bus1" in cols else None
            name_col = "name" if "name" in cols else None
            if not bus1_col or not name_col:
                return
            kw_ok = kw_col in cols
            kvar_ok = kvar_col in cols if kvar_col else False
            for _, row in df.iterrows():
                elem_bus = _bus_from_bus1(row.get(bus1_col, ""))
                if elem_bus not in buses:
                    continue
                rec: Dict[str, Any] = {
                    "bus": elem_bus,
                    "element_type": element_type,
                    "name": row.get(name_col, ""),
                    "kw": _safe_float(row.get(kw_col)) if kw_ok else 0.0,
                    "kvar": _safe_float(row.get(kvar_col)) if kvar_ok else 0.0,
                }
                rows.append(rec)

        add_rows(self.loads_df, "load", "kw", "kvar")
        add_rows(self.generators_df, "generator", "kw", "kvar")
        add_rows(self.pvsystems_df, "pvsystem", "pmpp", None)
        add_rows(self.storage_df, "storage", "kwrated", None)

        if not rows:
            return pd.DataFrame(columns=["bus", "element_type", "name", "kw", "kvar"])
        return pd.DataFrame(rows)

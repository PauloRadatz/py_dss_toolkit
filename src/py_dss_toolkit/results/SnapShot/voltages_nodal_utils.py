import pandas as pd
from py_dss_interface import DSS
from typing import Tuple
import math
import numpy as np

def create_nodal_voltage_records(dss: DSS) -> Tuple[dict, dict, list]:
    bus_nodes = dict()
    bus_vmags = dict()
    bus_vangs = dict()

    buses = [bus.lower().split(".")[0] for bus in dss.circuit.buses_names]

    for bus in buses:
        dss.circuit.set_active_bus(bus)
        num_nodes = dss.bus.num_nodes
        nodes = dss.bus.nodes
        vmags = dss.bus.vmag_angle_pu[: 2 * num_nodes: 2]
        vangs = dss.bus.vmag_angle_pu[1: 2 * num_nodes: 2]

        bus_nodes[bus] = nodes
        bus_vmags[bus] = vmags
        bus_vangs[bus] = vangs

    vmags_records = {
        bus: {f'node{node}': bus_vmags[bus][order] for order, node in enumerate(nodes)}
        for bus, nodes in bus_nodes.items()
    }

    vangs_records = {
        bus: {f'node{node}': bus_vangs[bus][order] for order, node in enumerate(nodes)}
        for bus, nodes in bus_nodes.items()
    }

    return vmags_records, vangs_records, buses

def create_nodal_voltage_dataframes(dss: DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    vmags_records, vangs_records, buses = create_nodal_voltage_records(dss)

    vmags_df = pd.DataFrame.from_dict(vmags_records, orient='index')
    vmags_df = vmags_df.reindex(buses)

    vangs_df = pd.DataFrame.from_dict(vangs_records, orient='index')
    vangs_df = vangs_df.reindex(buses)

    return vmags_df, vangs_df

def create_nodal_ll_voltage_records(dss: DSS) -> Tuple[dict, dict, list]:
    bus_nodes = dict()
    bus_vmags = dict()
    bus_vangs = dict()

    buses = [bus.lower().split(".")[0] for bus in dss.circuit.buses_names]

    for bus in buses:
        dss.circuit.set_active_bus(bus)
        num_nodes = dss.bus.num_nodes
        nodes = dss.bus.nodes
        cplx_pu_vll = dss.bus.pu_vll

        vmags = []
        vangs = []
        if cplx_pu_vll[0] != -99999.0:
            for i in range(0,len(cplx_pu_vll)-1,2):
                vmags.append(abs(cplx_pu_vll[i] + 1j * cplx_pu_vll[i+1]))
                vangs.append(math.degrees(math.atan2(cplx_pu_vll[i+1] , cplx_pu_vll[i])))

            bus_nodes[bus] = nodes
            bus_vmags[bus] = vmags
            bus_vangs[bus] = vangs

    vmags_records = {}
    for bus, nodes in bus_nodes.items():
        row = {}
        for order, node in enumerate(nodes):
            try:
                row[f'node{node}'] = bus_vmags[bus][order]
            except (IndexError, KeyError):
                row[f'node{node}'] = np.nan
        vmags_records[bus] = row

    vangs_records = {}
    for bus, nodes in bus_nodes.items():
        row = {}
        for order, node in enumerate(nodes):
            try:
                row[f'node{node}'] = bus_vangs[bus][order]
            except (IndexError, KeyError):
                row[f'node{node}'] = np.nan
        vangs_records[bus] = row

    return vmags_records, vangs_records, buses

def create_nodal_ll_voltage_dataframes(dss: DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    vmags_records, vangs_records, buses = create_nodal_ll_voltage_records(dss)

    vmags_df = pd.DataFrame.from_dict(vmags_records, orient='index')
    vmags_df = vmags_df.reindex(buses)

    vangs_df = pd.DataFrame.from_dict(vangs_records, orient='index')
    vangs_df = vangs_df.reindex(buses)

    return vmags_df, vangs_df


def create_nodal_smart_voltage_dataframes(
    dss: DSS,
    connection_type_map: dict,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Per-bus LN or LL voltage selection based on *connection_type_map*.

    For each bus, picks the LN or LL row according to
    ``connection_type_map.get(bus, 'ln')``.  No graph import needed.
    """
    ln_vmags, ln_vangs = create_nodal_voltage_dataframes(dss)
    ll_vmags, ll_vangs = create_nodal_ll_voltage_dataframes(dss)

    buses = [b.lower() for b in dss.circuit.buses_names]

    vmags_rows = {}
    vangs_rows = {}

    for bus_name in buses:
        conn_type = connection_type_map.get(bus_name, "ln")
        use_ll = (
            conn_type == "ll"
            and bus_name in ll_vmags.index
            and not ll_vmags.loc[bus_name].isna().all()
        )

        if use_ll:
            vmags_rows[bus_name] = ll_vmags.loc[bus_name]
            vangs_rows[bus_name] = ll_vangs.loc[bus_name]
        elif bus_name in ln_vmags.index:
            vmags_rows[bus_name] = ln_vmags.loc[bus_name]
            vangs_rows[bus_name] = ln_vangs.loc[bus_name]

    vmags_df = pd.DataFrame.from_dict(vmags_rows, orient="index")
    vmags_df = vmags_df.reindex(buses)

    vangs_df = pd.DataFrame.from_dict(vangs_rows, orient="index")
    vangs_df = vangs_df.reindex(buses)

    return vmags_df, vangs_df

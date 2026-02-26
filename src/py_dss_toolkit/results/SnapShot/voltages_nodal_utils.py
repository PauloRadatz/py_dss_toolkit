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

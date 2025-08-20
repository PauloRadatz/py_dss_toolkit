import pandas as pd
from py_dss_interface import DSS
from typing import Tuple
import math
import numpy as np

def create_nodal_voltage_dataframes(dss: DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    node_order = [node.lower() for node in dss.circuit.y_node_order]
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

    vmags_df = pd.DataFrame(index=buses)

    for bus, nodes in bus_nodes.items():
        for order, node in enumerate(nodes):
            column_name = f'node{node}'
            vmags_df.loc[bus, column_name] = bus_vmags[bus][order]

    vangs_df = pd.DataFrame(index=buses)

    for bus, nodes in bus_nodes.items():
        for order, node in enumerate(nodes):
            column_name = f'node{node}'
            vangs_df.loc[bus, column_name] = bus_vangs[bus][order]

    return vmags_df, vangs_df

def create_nodal_ll_voltage_dataframes(dss: DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    node_order = [node.lower() for node in dss.circuit.y_node_order]
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

    vmags_df = pd.DataFrame(index=buses)

    for bus, nodes in bus_nodes.items():
        for order, node in enumerate(nodes):
            column_name = f'node{node}'
            try:
                vmags_df.loc[bus, column_name] = bus_vmags[bus][order]
            except:
                vmags_df.loc[bus, column_name] = np.nan

    vangs_df = pd.DataFrame(index=buses)

    for bus, nodes in bus_nodes.items():
        for order, node in enumerate(nodes):
            column_name = f'node{node}'
            try:
                vangs_df.loc[bus, column_name] = bus_vangs[bus][order]
            except:
                vmags_df.loc[bus, column_name] = np.nan

    return vmags_df, vangs_df

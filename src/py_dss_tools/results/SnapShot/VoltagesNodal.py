# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageLNNodes.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple

class VoltagesNodal:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def voltage_ln_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def __create_dataframe(self):
        node_order = [node.lower() for node in self._dss.circuit.y_node_order]
        bus_nodes = dict()
        bus_vmags = dict()
        bus_vangs = dict()

        buses = [bus.lower().split(".")[0] for bus in self._dss.circuit.buses_names]

        for bus in buses:
            self._dss.circuit.set_active_bus(bus)
            num_nodes = self._dss.bus.num_nodes
            nodes = self._dss.bus.nodes
            vmags = self._dss.bus.vmag_angle_pu[: 2 * num_nodes: 2]
            vangs = self._dss.bus.vmag_angle_pu[1: 2 * num_nodes: 2]

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
            for node in nodes:
                column_name = f'node{node}'
                vangs_df.loc[bus, column_name] = bus_vangs[bus][0]

        return vmags_df, vangs_df

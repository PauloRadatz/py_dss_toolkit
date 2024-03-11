# -*- coding: utf-8 -*-
# @Time    : 3/11/2024 3:10 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : ResultsUtils.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd


class ResultsUtils:

    def __init__(self, dss: DSS):
        self._dss = dss

    def circuit_vmag_vang_dfs(self):
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

    def circuit_p_q_dfs(self):
        node_order = [node.lower() for node in self._dss.circuit.y_node_order]
        element_nodes = dict()
        element_p = dict()
        element_q = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            num_phases = self._dss.cktelement.num_phases
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = self.__create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            p = self._dss.cktelement.powers[: 2 * num_terminals * num_conductors: 2]
            q = self._dss.cktelement.powers[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_p[element] = p
            element_q[element] = q
            elements.append(element)

            if not self._dss.circuit.pd_element_next():
                is_there_pd = False

        is_there_pc = self._dss.circuit.pc_element_first()
        while is_there_pc:
            element = self._dss.cktelement.name.lower()
            num_phases = self._dss.cktelement.num_phases
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = self.__create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            p = self._dss.cktelement.powers[: 2 * num_terminals * num_conductors: 2]
            q = self._dss.cktelement.powers[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_p[element] = p
            element_q[element] = q
            elements.append(element)

            if not self._dss.circuit.pc_element_next():
                is_there_pc = False

        p_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                p_df.loc[element, node] = element_p[element][order]

        q_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                q_df.loc[element, node] = element_q[element][order]

        return p_df, q_df

    def circuit_imag_iang_dfs(self):
        node_order = [node.lower() for node in self._dss.circuit.y_node_order]
        element_nodes = dict()
        element_imags = dict()
        element_iangs = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            num_phases = self._dss.cktelement.num_phases
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = self.__create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            imags = self._dss.cktelement.currents_mag_ang[: 2 * num_terminals * num_conductors: 2]
            iangs = self._dss.cktelement.currents_mag_ang[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_imags[element] = imags
            element_iangs[element] = iangs
            elements.append(element)

            if not self._dss.circuit.pd_element_next():
                is_there_pd = False

        is_there_pc = self._dss.circuit.pc_element_first()
        while is_there_pc:
            element = self._dss.cktelement.name.lower()
            num_phases = self._dss.cktelement.num_phases
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = self.__create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            imags = self._dss.cktelement.currents_mag_ang[: 2 * num_terminals * num_conductors: 2]
            iangs = self._dss.cktelement.currents_mag_ang[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_imags[element] = imags
            element_iangs[element] = iangs
            elements.append(element)

            if not self._dss.circuit.pc_element_next():
                is_there_pc = False

        imags_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                imags_df.loc[element, node] = element_imags[element][order]

        iangs_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                iangs_df.loc[element, node] = element_iangs[element][order]

        return imags_df, iangs_df

    def __create_terminal_list(self, nodes, num_terminals):
        terminal_list = []
        for i, node in enumerate(nodes):
            terminal_number = int((i // (len(nodes) / num_terminals))) + 1
            terminal_list.append(f'Terminal{terminal_number}.{node}')

        return terminal_list

    def circuit_summary_df(self):
        p_feeder_kw = -self._dss.circuit.total_power[0]
        q_feeder_kvar = -self._dss.circuit.total_power[1]
        p_losses_feeder_kw = self._dss.circuit.losses[0] / 1000.0
        q_losses_feeder_kvar = self._dss.circuit.losses[1] / 1000.0
        max_v_pu = max(self._dss.circuit.buses_vmag_pu)
        min_v_pu = min(self._dss.circuit.buses_vmag_pu)

        data = {
            'P feeder (kW)': [p_feeder_kw],
            'Q feeder (kvar)': [q_feeder_kvar],
            'P losses (kW)': [p_losses_feeder_kw],
            'Q losses (kvar)': [q_losses_feeder_kvar],
            'max voltage (pu)': [max_v_pu],
            'min voltage (pu)': [min_v_pu]
        }

        df = pd.DataFrame(data)
        df = df.T.rename(columns={0: 'Results'})

        return df

    def energymeters_df(self):
        if self._dss.meters.count == 0:
            return None

        dict_to_df = dict()

        name_list = list()
        self._dss.meters.first()
        for _ in range(self._dss.meters.count):
            if self._dss.cktelement.is_enabled:
                name_list.append(self._dss.meters.name.lower())
                self._dss.meters.next()
        dict_to_df["name"] = name_list

        for index, element_property in enumerate(self._dss.meters.register_names):
            property_list = list()

            self._dss.meters.first()
            for _ in range(self._dss.meters.count):
                property_list.append(self._dss.meters.register_values[index])
                self._dss.meters.next()

            dict_to_df[element_property.lower()] = property_list

        return pd.DataFrame().from_dict(dict_to_df)

    def monitor_df(self, name: str):

        self._dss.monitors.name = name
        num_channels = self._dss.monitors.num_channels
        headers = self._dss.monitors.header
        dbl_hour = self._dss.monitors.dbl_hour
        dbl_freq = self._dss.monitors.dbl_freq

        dict_to_df = dict()
        dict_to_df["Hour"] = dbl_hour

        if len(dbl_freq) == 1:
            dict_to_df["sec"] = 0.0
        else:
            dict_to_df["sec"] = dbl_freq
        for index, header in enumerate(headers):
            dict_to_df[header] = self._dss.monitors.channel(index + 1)

        return pd.DataFrame().from_dict(dict_to_df)

# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ModelTools.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from typing import Dict


class ModelTools:

    def __init__(self, dss: DSS):
        self._dss = dss

    def buses_data_df(self):
        buses = self._dss.circuit.buses_names

        dict_to_df = dict()

        bus_properties = ["name", "nodes", "num_nodes", "kv_base", "distance",
                          "coord_defined", "x", "y", "latitude", "longitude",
                          "all_pce_active_bus", "all_pde_active_bus", "line_list", "line_total_miles", "load_list",
                          "section_id", "total_customers", "unique_node_number"]

        for bus_property in bus_properties:
            property_list = list()

            for bus in buses:
                self._dss.circuit.set_active_bus(bus)
                property_list.append(getattr(self._dss.bus, bus_property))

            dict_to_df[bus_property.lower()] = property_list

        return pd.DataFrame().from_dict(dict_to_df)

    def element_data(self, element_class: str, element_name: str) -> pd.DataFrame:
        self.__is_element_in_model(element_class, element_name)

        self._dss.text(f"select {element_class}.{element_name}")

        element_properties = self._dss.cktelement.property_names

        dict_to_df = dict()
        dict_to_df["name"] = element_name

        for element_property in element_properties:
            property_list = list()

            property_list.append(
                self._dss.dssproperties.value_read(
                    str(self._dss.cktelement.property_names.index(element_property) + 1)))

            dict_to_df[element_property.lower()] = property_list

        df = pd.DataFrame().from_dict(dict_to_df)
        df.set_index("name", inplace=True)

        return df.T

    def edit_element(self, element_class: str, element_name: str, properties: Dict[str, str]) -> None:
        self.__is_element_in_model(element_class, element_name)

        self._dss.text(f"select {element_class}.{element_name}")
        element_properties = self._dss.cktelement.property_names

        dss_string = f"edit {element_class}.{element_name} "

        for p, v in properties.items():
            if p.lower() not in element_properties:
                raise ValueError(f"{element_class}.{element_name} does not have property {p}")
            dss_string = dss_string + f" {p}={v}"

        self._dss.text(dss_string)

    def __is_element_in_model(self, element_class: str, element_name: str):
        element_class = element_class.lower()
        element_name = element_name.lower()
        elements_list = [e.lower() for e in self._dss.circuit.elements_names]
        element_full_name = f"{element_class}.{element_name}"
        if element_full_name not in elements_list:
            raise ValueError(f"Model does not have the {element_class}.{element_name}")

    def add_element(self, element_class: str, element_name: str, properties: Dict[str, str]) -> None:
        dss_string = f"new {element_class}.{element_name} "
        for p, v in properties.items():
            dss_string = dss_string + f" {p}={v}"
        self._dss.text(dss_string)

    def element_data_df(self, element):
        if element.count == 0:
            return None

        element.first()
        element_properties = self._dss.cktelement.property_names

        dict_to_df = dict()

        name_list = list()
        element.first()
        for _ in range(element.count):
            if self._dss.cktelement.is_enabled:
                name_list.append(element.name.lower())
                element.next()
        dict_to_df["name"] = name_list

        for element_property in element_properties:
            property_list = list()

            element.first()
            for _ in range(element.count):
                property_list.append(
                    self._dss.dssproperties.value_read(
                        str(self._dss.cktelement.property_names.index(element_property) + 1)))
                element.next()

            dict_to_df[element_property.lower()] = property_list

        return pd.DataFrame().from_dict(dict_to_df)

    def segments_df(self):
        elements_names = self._dss.circuit.elements_names

        filtered_elements = [element for element in elements_names if
                             element.lower().startswith("transformer.") or
                             element.lower().startswith("line.") or
                             element.lower().startswith("reactor.")]

        elem_name_list = list()
        elem_bus1_list = list()
        elem_bus2_list = list()
        elem_type_list = list()
        elem_x1_list = list()
        elem_y1_list = list()
        elem_x2_list = list()
        elem_y2_list = list()
        for elem in filtered_elements:
            self._dss.circuit.set_active_element(elem)
            elem_name_list.append(self._dss.cktelement.name.lower())
            elem_bus1_list.append(self._dss.cktelement.bus_names[0].split(".")[0])
            elem_bus2_list.append(self._dss.cktelement.bus_names[1].split(".")[0])
            elem_type_list.append(self._dss.cktelement.name.lower().split(".")[0])

            self._dss.circuit.set_active_bus(elem_bus1_list[-1])
            elem_x1_list.append(self._dss.bus.x)
            elem_y1_list.append(self._dss.bus.y)

            self._dss.circuit.set_active_bus(elem_bus2_list[-1])
            elem_x2_list.append(self._dss.bus.x)
            elem_y2_list.append(self._dss.bus.y)

        dict_df = dict()
        dict_df["name"] = elem_name_list
        dict_df["bus1"] = elem_bus1_list
        dict_df["bus2"] = elem_bus2_list
        dict_df["type"] = elem_type_list
        dict_df["x1"] = elem_x1_list
        dict_df["y1"] = elem_y1_list
        dict_df["x2"] = elem_x2_list
        dict_df["y2"] = elem_y2_list

        return pd.DataFrame.from_dict(dict_df)

    def summary_df(self):
        r_dict = dict()
        r_order = ["buses", "nodes", "ckt elements"]
        r_dict[r_order[0]] = self._dss.circuit.num_buses
        r_dict[r_order[1]] = self._dss.circuit.num_nodes
        r_dict[r_order[2]] = self._dss.circuit.num_ckt_elements

        elements_list = self._dss.circuit.elements_names

        element_counts = dict()

        for item in elements_list:
            self._dss.circuit.set_active_element(item)
            if self._dss.cktelement.is_enabled:
                element_class = item.split(".")[0]
                if element_class in element_counts:
                    element_counts[element_class] += 1
                else:
                    element_counts[element_class] = 1

        for element_class, count in element_counts.items():
            r_order.append(f"{element_class.lower()}")
            r_dict[r_order[-1]] = count

        line_length = 0
        for element in elements_list:
            if element.split(".")[0].lower() == "line":
                self._dss.circuit.set_active_element(element)
                self._dss.lines.name = element.split(".")[1].lower()
                if self._dss.cktelement.is_enabled:
                    line_length += self._dss.lines.length

        max_line_norm_amps, min_line_norm_amps = self.get_max_min_norm_amps(elements_list, "line")
        max_transformer_norm_amps, min_transformer_norm_amps = self.get_max_min_norm_amps(elements_list, "transformer")
        max_reactor_norm_amps, min_reactor_norm_amps = self.get_max_min_norm_amps(elements_list, "reactor")

        r_dict["line length"] = line_length
        if min_line_norm_amps != 9999:
            r_dict["line min norm amps"] = min_line_norm_amps
            r_dict["line max norm amps"] = max_line_norm_amps
        if min_transformer_norm_amps != 9999:
            r_dict["transformer min norm amps"] = min_transformer_norm_amps
            r_dict["transformer max norm amps"] = max_transformer_norm_amps
        if min_reactor_norm_amps != 9999:
            r_dict["reactor min norm amps"] = min_reactor_norm_amps
            r_dict["reactor max norm amps"] = max_reactor_norm_amps

        max_load_kw = -9999
        min_load_kw = 9999
        for element in elements_list:
            if element.split(".")[0].lower() == "load":
                self._dss.circuit.set_active_element(element)
                self._dss.loads.name = element.split(".")[1].lower()
                if self._dss.cktelement.is_enabled:
                    load_kw = self._dss.loads.kw
                    if load_kw < min_load_kw:
                        min_load_kw = load_kw
                    if load_kw > max_load_kw:
                        max_load_kw = load_kw

        if min_load_kw != 9999:
            r_dict["load min kw"] = min_load_kw
            r_dict["load max kw"] = max_load_kw

        df = pd.DataFrame.from_dict(r_dict, orient='index', columns=['count'])
        return df

    def get_max_min_norm_amps(self, elements_list, element_type):
        max_norm_amps = -9999
        min_norm_amps = 9999
        for element in elements_list:
            if element.split(".")[0].lower() == element_type.lower():
                self._dss.circuit.set_active_element(element)
                if self._dss.cktelement.is_enabled:
                    norm_amps = self._dss.cktelement.norm_amps
                    if norm_amps < min_norm_amps:
                        min_norm_amps = norm_amps
                    if norm_amps > max_norm_amps:
                        max_norm_amps = norm_amps
        return max_norm_amps, min_norm_amps

    def add_meter(self, meter_name: str, element: str, terminal: int = 1):
        self._dss.text(f"new energymeter.{meter_name} element={element} terminal={terminal}")

    def add_line_in_vsource(self, add_meter=True):
        code = "unrealbus"
        self._dss.vsources.name = "source"
        feeder_head_bus = self._dss.cktelement.bus_names[0].split('.')[0].lower()
        self._dss.circuit.set_active_bus(feeder_head_bus)
        x = self._dss.bus.x
        y = self._dss.bus.y

        if feeder_head_bus.split("_")[-1] != code:
            self._dss.text(f'Edit Vsource.source bus1={feeder_head_bus}_{code}')
            self._dss.text(f'New Line.feeder_head bus1={feeder_head_bus}_{code} bus2={feeder_head_bus} Switch=True')

            self._dss.text("MakebusList")

            self._dss.circuit.set_active_bus(f'{feeder_head_bus}_{code}')
            self._dss.bus.x = x
            self._dss.bus.y = y

            existing_meter = False
            self._dss.meters.first()
            for meter in self._dss.meters.names:
                if meter != "NONE":
                    self._dss.circuit.set_active_element(f"energymeter.{meter}")
                    if self._dss.cktelement.is_enabled:
                        existing_meter = True
                        break
            if not existing_meter and add_meter:
                self.add_meter("meter_feeder_head", "Line.feeder_head", terminal=1)

            self._dss.text("calcvoltagebase")

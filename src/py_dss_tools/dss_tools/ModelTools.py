# -*- coding: utf-8 -*-
# @Time    : 3/12/2024 6:35 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
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
                             element.lower().startswith("transformer.") or element.lower().startswith("line.")]

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

    def summary_data(self):
        r_dict = dict()
        r_order = ["buses", "nodes", "ckt elements"]
        r_dict[r_order[0]] = self._dss.circuit.num_buses
        r_dict[r_order[1]] = self._dss.circuit.num_nodes
        r_dict[r_order[2]] = self._dss.circuit.num_ckt_elements

        elements_list = self._dss.circuit.elements_names

        element_counts = dict()

        for item in elements_list:
            element_class = item.split(".")[0]
            if element_class in element_counts:
                element_counts[element_class] += 1
            else:
                element_counts[element_class] = 1

        for element_class, count in element_counts.items():
            r_order.append(f"{element_class.lower()}")
            r_dict[r_order[-1]] = count

        df = pd.DataFrame.from_dict(r_dict, orient='index', columns=['count'])
        return df

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

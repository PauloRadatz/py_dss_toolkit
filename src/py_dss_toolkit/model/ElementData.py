# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Dict

import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.ModelUtils import ModelUtils


class ElementData:
    def __init__(self, dss: DSS):
        self._dss = dss
        self._model_utils = ModelUtils(dss)

    def _element_data_records(self, element_class: str, element_name: str) -> dict:
        if self._model_utils.is_element_in_model(element_class, element_name):

            self._dss.text(f"select {element_class}.{element_name}")

            element_properties = self._dss.cktelement.property_names

            records = dict()
            records["name"] = element_name

            for index, element_property in enumerate(element_properties, start=1):
                records[element_property.lower()] = [self._dss.dssproperties.value_read(str(index))]

            return records

        else:
            raise ValueError(f"{element_class}.{element_name} does not exist in the model")

    def element_data(self, element_class: str, element_name: str) -> pd.DataFrame:
        records = self._element_data_records(element_class, element_name)

        df = pd.DataFrame.from_dict(records)
        df.set_index("name", inplace=True)

        return df.T

    def edit_element(self, element_class: str, element_name: str, properties: Dict[str, str]) -> None:
        if self._model_utils.is_element_in_model(element_class, element_name):

            self._dss.text(f"select {element_class}.{element_name}")
            element_properties = [prop.lower() for prop in self._dss.cktelement.property_names]

            dss_string = f"edit {element_class}.{element_name} "

            for p, v in properties.items():
                if p.lower() not in element_properties:
                    raise ValueError(f"{element_class}.{element_name} does not have property {p}")
                dss_string = dss_string + f" {p}={v}"

            self._dss.text(dss_string)
        else:
            raise ValueError(f"{element_class}.{element_name} does not exist in the model")

    def add_element(self, element_class: str, element_name: str, properties: Dict[str, str]) -> None:
        if self._model_utils.is_element_in_model(element_class, element_name):
            raise ValueError(f"{element_class}.{element_name} already exists in the model")
        dss_string = f"new {element_class}.{element_name} "
        for p, v in properties.items():
            dss_string = dss_string + f" {p}={v}"
        self._dss.text(dss_string)

    def add_line_in_vsource(self, add_meter=False, add_monitors=False):
        code = "unrealbus"
        self._dss.vsources.name = "source"
        feeder_head_bus = self._dss.cktelement.bus_names[0].split('.')[0].lower()
        self._dss.circuit.set_active_bus(feeder_head_bus)
        x = self._dss.bus.x
        y = self._dss.bus.y

        if feeder_head_bus.split("_")[-1] == code:
            raise ValueError(
                f"The feeder head bus '{feeder_head_bus}' already ends with '_unrealbus'. "
                "You have probably already used add_line_in_vsource before. "
                "This operation cannot be applied twice."
            )
        else:
            self._dss.text(f'Edit Vsource.source bus1={feeder_head_bus}_{code}')
            self._dss.text(f'New Line.feeder_head bus1={feeder_head_bus}_{code} bus2={feeder_head_bus} Switch=True')

            self._dss.text("MakebusList")

            self._dss.circuit.set_active_bus(f'{feeder_head_bus}_{code}')
            self._dss.bus.x = x
            self._dss.bus.y = y

            existing_meter = False
            self._dss.meters.first()
            for meter in self._dss.meters.names:
                if meter.lower() != "NONE".lower():
                    self._dss.circuit.set_active_element(f"energymeter.{meter}")
                    if self._dss.cktelement.is_enabled:
                        existing_meter = True
                        break
            if not existing_meter and add_meter:
                self.__add_meter("meter_feeder_head", "Line.feeder_head", terminal=1)

            self._dss.text("calcvoltagebase")

            if add_monitors:
                self.__add_monitor("monitor_feeder_head_pq", "Line.feeder_head", terminal=1, mode=1)
                self.__add_monitor("monitor_feeder_head_vi", "Line.feeder_head", terminal=1, mode=0)

    def __add_monitor(self, monitor_name: str, element: str, terminal: int, mode: int, vipolar: bool = True,
                      ppolar: bool = False):
        self._dss.text(f"new monitor.{monitor_name} element={element} terminal={terminal}, mode={mode} "
                       f"vipolar={'yes' if vipolar else 'no'} ppolar={'yes' if ppolar else 'no'}")

    def __add_meter(self, meter_name: str, element: str, terminal: int = 1):
        self._dss.text(f"new energymeter.{meter_name} element={element} terminal={terminal}")

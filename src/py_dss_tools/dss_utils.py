# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : dss_utils.py
# @Software: PyCharm


from dataclasses import dataclass
from typing import Optional, Union
from py_dss_interface import DSS


class DSSUtils:

    def __init__(self, dss: DSS):
        self._dss = dss

    def update_dss(self, dss: DSS):
        self._dss = dss

    def compile_dss(self, dss_file: str):
        self._dss.text("ClearAll")
        self._dss.text("Compile " + "[" + dss_file + "]")

    def solve_snapshot(self, control_mode="Static", max_control_iter=10):
        self._dss.text("Set maxcontroliter=" + str(max_control_iter))
        self._dss.text("set ControlMode=" + control_mode)
        self._dss.text("Set Mode=SnapShot")
        self._dss.text("solve")

    def dss_command(self, command: str):
        self._dss.text(command)

    def add_meter(self, meter_name: str, element: str, terminal: int = 1):
        self._dss.text(f"new energymeter.{meter_name} element={element} terminal={terminal}")

    def batchedit(self, element_type: str, property: str, value: str):
        self._dss.text(f"batchedit {element_type}..* {property}={value}")

    def calc_voltage_base(self):
        self._dss.text("calcvoltagebase")

    def save_circuit(self, output_dir: Optional[str] = None, case_name: Optional[str] = None):
        if output_dir:
            self._dss.dssinterface.datapath = f"{output_dir}"

        if case_name:
            self._dss.text(f"set casename='{case_name}'")
            self._dss.text(f"save circuit Dir={case_name}")
        else:
            self._dss.text(f"save circuit")

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

            self.calc_voltage_base()


dss_utils = DSSUtils(None)

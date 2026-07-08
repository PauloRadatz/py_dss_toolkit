# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageSettings.py
# @Software: PyCharm

from dataclasses import dataclass
from dataclasses import field

from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.BaseSettingsNumerical import BaseSettingsNumerical
from py_dss_toolkit.view.view_base.VoltageProfileBase import VOLTAGE_TYPE


@dataclass(kw_only=True)
class VoltageSettings(BaseSettingsNumerical):
    colorbar_title: str = field(init=True, repr=True, default="Voltage (pu)")
    bus: str = field(init=True, repr=True, default="bus2")
    nodes_voltage_value: str = field(init=True, repr=True, default="mean")
    voltage_type: VOLTAGE_TYPE = field(init=True, repr=True, default="ln")

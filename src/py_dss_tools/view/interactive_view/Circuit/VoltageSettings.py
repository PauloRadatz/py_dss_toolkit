# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageSettings.py
# @Software: PyCharm

from dataclasses import dataclass, field
from typing import Optional, Union, Tuple, List
from py_dss_tools.view.interactive_view.Circuit.BaseSettingsNumerical import BaseSettingsNumerical

@dataclass(kw_only=True)
class VoltageSettings(BaseSettingsNumerical):
    colorbar_title: str = field(init=True, repr=True, default="Voltage (pu)")

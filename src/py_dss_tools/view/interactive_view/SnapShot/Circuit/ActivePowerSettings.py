# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ActivePowerSettings.py
# @Software: PyCharm

from dataclasses import dataclass, field
from py_dss_tools.view.interactive_view.SnapShot.Circuit.BaseSettingsNumerical import BaseSettingsNumerical

@dataclass(kw_only=True)
class ActivePowerSettings(BaseSettingsNumerical):
    colorbar_title: str = field(init=True, repr=True, default="Active Power (kW)")


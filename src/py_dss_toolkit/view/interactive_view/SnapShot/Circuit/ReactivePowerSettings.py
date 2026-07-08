# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ReactivePowerSettings.py
# @Software: PyCharm

from dataclasses import dataclass
from dataclasses import field

from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.BaseSettingsNumerical import BaseSettingsNumerical


@dataclass(kw_only=True)
class ReactivePowerSettings(BaseSettingsNumerical):
    colorbar_title: str = field(init=True, repr=True, default="Reactive Power (kvar)")

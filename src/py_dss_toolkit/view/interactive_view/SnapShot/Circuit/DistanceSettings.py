# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass
from dataclasses import field

from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.BaseSettingsNumerical import BaseSettingsNumerical


@dataclass(kw_only=True)
class DistanceSettings(BaseSettingsNumerical):
    colorbar_title: str = field(init=True, repr=True, default="Distance from Meter (km)")

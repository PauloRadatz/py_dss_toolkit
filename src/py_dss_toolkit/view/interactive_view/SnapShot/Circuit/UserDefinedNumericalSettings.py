# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : UserDefinedNumericalSettings.py
# @Software: PyCharm

from dataclasses import dataclass, field
from typing import Optional
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.BaseSettingsNumerical import BaseSettingsNumerical
import pandas as pd

@dataclass(kw_only=True)
class UserDefinedNumericalSettings(BaseSettingsNumerical):
    _parameter: str = field(init=False, repr=True, default="User Numerical Defined")
    unit: str = field(init=True, repr=True, default="Unit")
    colorbar_title: Optional[str] = field(init=True, repr=True, default=None)
    results: Optional[pd.DataFrame] = field(init=True, repr=True, default=None)
    num_decimal_points: int = field(init=True, repr=True, default=2)
    colorbar_title: str =  field(init=True, repr=True, default="Colorbar Title")

    def __post_init__(self):
        self._parameter = "User Numerical Defined"

    @property
    def parameter(self) -> str:
        return self._parameter

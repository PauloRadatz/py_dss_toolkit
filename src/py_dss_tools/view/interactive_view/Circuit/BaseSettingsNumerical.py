# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : BaseSettingsNumerical.py
# @Software: PyCharm

from dataclasses import dataclass, field
from typing import Optional, Union, Tuple, List

@dataclass(kw_only=True)
class BaseSettingsNumerical:
    colorbar_cmin: Optional[float] = field(init=True, default=None, repr=True)
    colorbar_cmax: Optional[float] = field(init=True, default=None, repr=True)
    colorbar_tickvals: Optional[int] = field(init=True, default=None, repr=True)
    colorbar_ticktext_decimal_points: Optional[int] = field(init=True, default=None, repr=True)
    colorbar_tickvals_list: Optional[List[float]] = field(init=True, default=None, repr=True)
    colorscale: str = field(init=True, repr=True, default="jet_r")  # https://plotly.com/python/builtin-colorscales/

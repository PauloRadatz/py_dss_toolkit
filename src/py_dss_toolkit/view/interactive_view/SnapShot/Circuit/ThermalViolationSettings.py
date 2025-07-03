# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass, field
from typing import Optional, Union, Tuple, List, Dict
import pandas as pd


@dataclass(kw_only=True)
class ThermalViolationSettings:
    color_map: dict = field(init=True, repr=True, default_factory=lambda: {
        '0': ["Normal", "blue"],
        '1': ["Abnormal", "red"],
    })
    legendgrouptitle_text: str = field(init=True, repr=True, default_factory=lambda: "Thermal Violations")

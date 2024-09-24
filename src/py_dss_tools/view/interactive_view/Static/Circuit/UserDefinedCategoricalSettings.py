# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : UserDefinedCategoricalSettings.py
# @Software: PyCharm

from dataclasses import dataclass, field
from typing import Optional, Union, Tuple, List, Dict
import pandas as pd


@dataclass(kw_only=True)
class UserDefinedCategoricalSettings:
    _parameter: str = field(init=False, repr=True, default="User Categorical Defined")
    results: Optional[pd.DataFrame] = field(init=True, repr=True, default=None)
    color_map: Optional[dict] = field(init=True, repr=True, default=None)
    legendgrouptitle_text: str = field(init=True, repr=True, default_factory=lambda: "Legend Title")

    def __post_init__(self):
        self._parameter = "User Categorical Defined"

    @property
    def parameter(self) -> str:
        return self._parameter

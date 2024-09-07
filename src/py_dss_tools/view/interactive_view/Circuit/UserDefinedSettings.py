# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : UserDefinedSettings.py
# @Software: PyCharm

from dataclasses import dataclass, field
from typing import Optional, Union, Tuple, List
from py_dss_tools.view.interactive_view.Circuit.BaseSettingsNumerical import BaseSettingsNumerical
import pandas as pd

@dataclass(kw_only=True)
class UserDefinedSettingsSettings(BaseSettingsNumerical):
    colorbar_title: Optional[str] = field(init=True, repr=True, default=None)
    results: Optional[pd.DataFrame] = field(init=True, repr=True, default=None)

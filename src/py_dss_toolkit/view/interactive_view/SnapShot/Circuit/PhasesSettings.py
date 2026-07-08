# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PhasesSettings.py
# @Software: PyCharm

from dataclasses import dataclass
from dataclasses import field


@dataclass(kw_only=True)
class PhasesSettings:
    color_map: dict = field(
        init=True,
        repr=True,
        default_factory=lambda: {
            "4": ["4-phases", "purple"],
            "3": ["3-phases", "blue"],
            "2": ["2-phases", "red"],
            "1": ["1-phase", "green"],
        },
    )
    legendgrouptitle_text: str = field(init=True, repr=True, default_factory=lambda: "Line Phases")

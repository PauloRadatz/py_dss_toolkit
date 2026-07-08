# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass
from dataclasses import field


@dataclass(kw_only=True)
class ThermalViolationSettings:
    color_map: dict = field(
        init=True,
        repr=True,
        default_factory=lambda: {
            "0": ["Normal", "blue"],
            "1": ["Abnormal", "red"],
        },
    )
    legendgrouptitle_text: str = field(init=True, repr=True, default_factory=lambda: "Thermal Violations")

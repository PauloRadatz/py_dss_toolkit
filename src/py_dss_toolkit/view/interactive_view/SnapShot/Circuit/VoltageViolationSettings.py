# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass
from dataclasses import field


@dataclass(kw_only=True)
class VoltageViolationSettings:
    color_map: dict = field(
        init=True,
        repr=True,
        default_factory=lambda: {
            "0": ["Normal", "blue"],
            "1": ["Under Voltage", "purple"],
            "2": ["Over Voltage", "red"],
            "3": ["Under and Over Voltages", "orange"],
        },
    )
    legendgrouptitle_text: str = field(init=True, repr=True, default_factory=lambda: "Voltage Violations")

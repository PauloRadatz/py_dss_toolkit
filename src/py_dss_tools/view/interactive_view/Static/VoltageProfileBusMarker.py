# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfileBusMarker.py
# @Software: PyCharm

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class VoltageProfileBusMarker:
    name: str = field(init=True, repr=True)
    symbol: str = field(init=True, repr=True, default="circle")
    size: float = field(init=True, repr=True, default=10)
    color: str = field(init=True, repr=True, default="black")
    annotate: bool = field(init=True, repr=True, default=False)
    marker_name: str = field(init=True, repr=True, default=name)
    show_legend: bool = field(init=True, repr=True, default=False)

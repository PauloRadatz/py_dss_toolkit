# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : CircuitBusMarker.py
# @Software: PyCharm

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class CircuitBusMarker:
    name: str = field(init=True, repr=True)
    symbol: str = field(init=True, repr=True, default="circle")
    size: float = field(init=True, repr=True, default=10)
    color: str = field(init=True, repr=True, default="black")
    marker_name: str = field(init=True, repr=True, default=name)

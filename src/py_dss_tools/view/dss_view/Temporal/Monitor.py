# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : MonitorBase.py
# @Software: PyCharm

import matplotlib.pyplot as plt
from py_dss_interface import DSS
from typing import Optional, Union, Tuple
from py_dss_tools.view.view_base.MonitorBase import MonitorBase


class Monitor(MonitorBase):

    def __init__(self, dss: DSS):
        self._dss = dss

        MonitorBase.__init__(self, self._dss, None)

    def vmag_vs_time(self,
                     name: str,
                     unit: str = "pu"):
        self._check_v_monitor(name)

        elem_nodes, v_base = self._organize_v_results(name)

        if len(elem_nodes) == 1:
            channels = "[1]"
            bases = f"[{v_base}]"
        elif len(elem_nodes) == 2:
            channels = "[1 3]"
            bases = f"[{v_base} {v_base}]"
        elif len(elem_nodes) == 3:
            channels = "[1 3 5]"
            bases = f"[{v_base} {v_base} {v_base}]"

        if unit == "pu":
            self._dss.text(f"plot monitor object={name} channels={channels} bases={bases}")
        else:
            self._dss.text(f"plot monitor object={name} channels={channels}")

    def p_vs_time(self, name: str):
        self._check_p_monitor(name)

        elem_nodes = self._organize_p_results(name)

        if len(elem_nodes) == 1:
            channels = "[1]"
        elif len(elem_nodes) == 2:
            channels = "[1 3]"
        elif len(elem_nodes) == 3:
            channels = "[1 3 5]"


        self._dss.text(f"plot monitor object={name} channels={channels}")

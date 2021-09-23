# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:04:50
 Project: py_dss_tools [set, 2021]
"""
class Reactor:
    name = "Reactor"
    name_plural = "Reactors"
    columns = []

    def __init__(self, dss):
        self.dss = dss

# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 03:26:21
 Project: py_dss_tools [set, 2021]
"""
from inspect import currentframe


class Utils:
    @staticmethod
    def get_linenumber():
        cf = currentframe()
        return cf.f_back.f_lineno

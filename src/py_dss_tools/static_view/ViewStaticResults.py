# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.static_view.VoltageProfile import VoltageProfile
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_interface import DSS


class ViewStaticResults(VoltageProfile):

    def __init__(self, dss: DSS, results: StaticResults):
        VoltageProfile.__init__(self, dss, results)

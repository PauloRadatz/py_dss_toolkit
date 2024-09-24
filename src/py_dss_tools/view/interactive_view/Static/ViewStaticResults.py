# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewStaticResults.py
# @Software: PyCharm

from py_dss_tools.view.interactive_view.Static.VoltageProfile import VoltageProfile
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_interface import DSS
from py_dss_tools.view.interactive_view.Static.Circuit.ViewCircuitResults import ViewCircuitResults
from py_dss_tools.model.ModelBase import ModelBase


class ViewStaticResults(VoltageProfile, ViewCircuitResults):

    def __init__(self, dss: DSS, results: StaticResults, model: [ModelBase]):
        VoltageProfile.__init__(self, dss, results)
        ViewCircuitResults.__init__(self, dss, results, model)

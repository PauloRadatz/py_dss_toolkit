# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.view.interactive_view.Static.ViewStaticResults import ViewStaticResults
from py_dss_tools.view.interactive_view.Temporal.ViewTemporalResults import ViewTemporalResults
from py_dss_tools.view.interactive_view.Static.Circuit import ViewCircuitResults
from py_dss_tools.results.Results import Results
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_tools.results.Temporal.TemporalResults import TemporalResults
from py_dss_tools.model.ModelBase import ModelBase
from py_dss_interface import DSS
from typing import Union


class ViewResults(ViewStaticResults, ViewTemporalResults):

    def __init__(self, dss: DSS, results: Union[Results, StaticResults, TemporalResults], model: [ModelBase]):
        ViewStaticResults.__init__(self, dss, results, model)
        ViewTemporalResults.__init__(self, dss, results)


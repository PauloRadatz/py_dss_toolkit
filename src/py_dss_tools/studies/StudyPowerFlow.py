# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PowerFlow.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.StaticResults import StaticResults
from py_dss_tools.visualization.ViewStaticResults import ViewStaticResults


class StudyPowerFlow(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = StaticResults(self._dss)
        self._view = ViewStaticResults(self._dss, self._results)

    @property
    def results(self):
        return self._results

    @property
    def view(self):
        return self._view

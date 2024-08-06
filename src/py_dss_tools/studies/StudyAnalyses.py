# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : StudyAnalyses.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.AnalysisFeederResults import AnalysisFeederResults
from dataclasses import dataclass


@dataclass(kw_only=True)
class StudyAnalysis(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = AnalysisFeederResults(self._dss) #exibe os resultados para a clesse e estudo criado

    @property
    def results(self):
        return self._results

   # @property
    #def view(self):
        #return self._view

#    def run(self):
#        self.__check_settings()
#       self.dss.text("solve")  #Acredito que não preciso definir nenhuma condição para execução da varredura

#    @property
#    def settings(self):
#        return self._settings

#    def __check_settings(self):
#        self.settings.mode = self.dss.text("get mode")

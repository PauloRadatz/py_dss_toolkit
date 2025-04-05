# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : StudyModelVerification.py
# @Software: PyCharm

from py_dss_toolkit.studies.StudyBase import StudyBase
from py_dss_toolkit.results.ModelVerification.ModelVerificationResults import ModelVerificationResults
from dataclasses import dataclass


@dataclass(kw_only=True)
class StudyModelVerification(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = ModelVerificationResults(self._dss)

    @property
    def results(self):
        return self._results

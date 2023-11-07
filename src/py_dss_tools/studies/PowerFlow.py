# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PowerFlow.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase


class PowerFlow(StudyBase):

    def __post_init__(self):
        super().__post_init__()

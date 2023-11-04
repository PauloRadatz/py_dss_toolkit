# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PowerFlow.py
# @Software: PyCharm

from py_dss_tools.secondary.StudyBase import StudyBase


class PowerFlow(StudyBase):

    def __init__(self, name, dss_file, frequency_base, dll):
        super().__init__(name, dss_file, frequency_base, dll)
